#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
UNESCO:
------

Reads UNESCO API and creates datasets.

"""

import logging

import time

import sys
from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.data.showcase import Showcase
from hdx.location.country import Country
from hdx.utilities.downloader import DownloadError
from six import reraise
from slugify import slugify

logger = logging.getLogger(__name__)

MAX_OBSERVATIONS = 2000
dataurl_suffix = 'format=sdmx-json&detail=structureonly&includeMetrics=true'


def get_countriesdata(base_url, downloader):
    response = downloader.download('%scodelist/UNESCO/CL_AREA/latest?format=sdmx-json' % base_url)
    jsonresponse = response.json()
    return jsonresponse['Codelist'][0]['items']


def get_endpoints_metadata(base_url, downloader, endpoints):
    endpoints_metadata = dict()
    for endpoint in sorted(endpoints):
        base_dataurl = '%sdata/UNESCO,%s,1.0/' % (base_url, endpoint)
        datastructure_url = '%s?%s' % (base_dataurl, dataurl_suffix)
        response = downloader.download(datastructure_url)
        json = response.json()
        indicator = json['structure']['name']
        dimensions = json['structure']['dimensions']['observation']
        urllist = [base_dataurl]
        for dimension in dimensions:
            if dimension['id'] == 'REF_AREA':
                urllist.append('%s')
            else:
                urllist.append('.')
        urllist.append('?')
        structure_url = ''.join(urllist)
        endpoints_metadata[endpoint] = indicator, structure_url, endpoints[endpoint]
    return endpoints_metadata


def generate_dataset_and_showcase(downloader, countrydata, endpoints_metadata):
    """
    https://api.uis.unesco.org/sdmx/data/UNESCO,DEM_ECO,1.0/....AU.?format=csv-:-tab-true-y&locale=en&subscription-key=...
    """
    countryiso2 = countrydata['id']
    countryname = countrydata['names'][0]['value']
    countryiso3 = Country.get_iso3_from_iso2(countryiso2)
    if countryiso3 is None:
        countryiso3, _ = Country.get_iso3_country_code_fuzzy(countryname)
        if countryiso3 is None:
            logger.exception('Cannot get iso3 code for %s!' % countryname)
            return None, None
        logger.info('Matched %s to %s!' % (countryname, countryiso3))
    name = 'UNESCO indicators for %s' % countryname
    slugified_name = slugify(name).lower()

    title = '%s - Sustainable development, Education, Demographic and Socioeconomic Indicators' % countryname
    dataset = Dataset({
        'name': slugified_name,
        'title': title
    })
    dataset.set_maintainer('196196be-6037-4488-8b71-d786adf4c081')
    dataset.set_organization('18f2d467-dcf8-4b7e-bffa-b3c338ba3a7c')
    try:
        dataset.add_country_location(countryiso3)
    except HDXError as e:
        logger.exception('%s has a problem! %s' % (countryname, e))
        return None, None
    dataset.set_expected_update_frequency('Every year')
    tags = ['indicators', 'UNESCO', 'sustainable development', 'demographic', 'socioeconomic', 'education']
    dataset.add_tags(tags)

    earliest_year = 10000
    latest_year = 0
    for endpoint in sorted(endpoints_metadata):
        time.sleep(0.2)
        indicator, structure_url, more_info_url = endpoints_metadata[endpoint]
        structure_url = structure_url % countryiso2
        response = None
        while response is None:
            try:
                response = downloader.download('%s%s' % (structure_url, dataurl_suffix))
            except DownloadError:
                exc_info = sys.exc_info()
                tp, val, tb = exc_info
                if 'Quota Exceeded' in str(val.__cause__):
                    logger.info('Sleeping for one minute')
                    time.sleep(60)
                else:
                    reraise(*exc_info)
        json = response.json()
        observations = json['structure']['dimensions']['observation']
        time_periods = dict()
        for observation in observations:
            if observation['id'] == 'TIME_PERIOD':
                for value in observation['values']:
                    time_periods[int(value['id'])] = value['actualObs']
        years = sorted(time_periods.keys(), reverse=True)
        if len(years) == 0:
            logger.warning('No time periods for endpoint %s for country %s!' % (indicator, countryname))
            continue
        end_year = years[0]
        if years[-1] < earliest_year:
            earliest_year = years[-1]
        if end_year > latest_year:
            latest_year = end_year
        csv_url = '%sformat=csv' % structure_url

        description = more_info_url
        if description != ' ':
            description = '[Info on %s](%s)' % (indicator, description)
        description = 'To save, right click download button & click Save Link/Target As  \n%s' % description

        def create_resource():
            url_years = '&startPeriod=%d&endPeriod=%d' % (start_year, end_year)
            resource = {
                'name': '%s (%d-%d)' % (indicator, start_year, end_year),
                'description': description,
                'format': 'csv',
                'url': downloader.get_full_url('%s%s' % (csv_url, url_years))
            }
            dataset.add_update_resource(resource)

        obs_count = 0
        start_year = end_year
        for year in years:
            obs_count += time_periods[year]
            if obs_count < MAX_OBSERVATIONS:
                start_year = year
                continue
            obs_count = time_periods[year]
            create_resource()
            end_year = year
        create_resource()

    if len(dataset.get_resources()) == 0:
        logger.error('No resources created for country %s!' % countryname)
        return None, None
    dataset.set_dataset_year_range(earliest_year, latest_year)

    showcase = Showcase({
        'name': '%s-showcase' % slugified_name,
        'title': 'Indicators for %s' % countryname,
        'notes': 'Education, literacy and other indicators for %s' % countryname,
        'url': 'http://uis.unesco.org/en/country/%s' % countryiso2,
        'image_url': 'http://www.tellmaps.com/uis/internal/assets/uisheader-en.png'
    })
    showcase.add_tags(tags)
    return dataset, showcase
