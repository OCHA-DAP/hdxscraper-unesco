#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
UNESCO:
------

Reads UNESCO API and creates datasets.

"""

import logging

from hdx.data.dataset import Dataset
from hdx.data.showcase import Showcase
from hdx.location.country import Country
from slugify import slugify

logger = logging.getLogger(__name__)


def get_countriesdata(base_url, downloader):
    response = downloader.download('%scodelist/UNESCO/CL_AREA/latest?format=sdmx-json' % base_url)
    jsonresponse = response.json()
    return jsonresponse['Codelist'][0]['items']


def generate_dataset_and_showcase(base_url, downloader, countrydata, endpoints):
    """
    https://api.uis.unesco.org/sdmx/data/UNESCO,DEM_ECO,1.0/....AU.?format=csv-:-tab-true-y&locale=en&subscription-key=...
    """
    countryiso2 = countrydata['id']
    countryname = countrydata['names'][0]['value']
    countryiso3 = Country.get_iso3_from_iso2(countryiso2)
    if countryiso3 is None:
        countryiso3, _ = Country.get_iso3_country_code_fuzzy(countryname)
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
    dataset.add_country_location(countryiso3)
    logger.info('Creating dataset: %s' % title)
    dataset.set_expected_update_frequency('Every year')
    tags = ['indicators', 'UNESCO', 'sustainable development', 'demographic', 'socioeconomic', 'education']
    dataset.add_tags(tags)

    earliest_year = 10000
    latest_year = 0
    for endpoint in sorted(endpoints):
        datastructure_url = '%sdataflow/UNESCO/%s/latest?references=datastructure&format=sdmx-json' % (base_url, endpoint)
        response = downloader.download(datastructure_url)
        json = response.json()
        indicator = json['Dataflow'][0]['names'][0]['value']
        dimensions = json['DataStructure'][0]['dimensionList']['dimensions']
        urllist = ['%sdata/UNESCO,%s,1.0/' % (base_url, endpoint)]
        for dimension in dimensions:
            if dimension['id'] == 'REF_AREA':
                urllist.append(countryiso2)
            else:
                urllist.append('.')
        urllist.append('?format=sdmx-json&detail=structureonly&includeMetrics=true')
        structure_url = ''.join(urllist)
        response = downloader.download(structure_url)
        json = response.json()
        observations = json['structure']['dimensions']['observation']
        time_periods = dict()
        for observation in observations:
            if observation['id'] == 'TIME_PERIOD':
                for value in observation['values']:
                    time_periods[int(value['id'])] = value['actualObs']
        years = sorted(time_periods.keys(), reverse=True)
        end_year = years[0]
        if years[-1] < earliest_year:
            earliest_year = years[-1]
        if end_year > latest_year:
            latest_year = end_year
        urllist[-1] = '?format=csv'
        urllist.append('')

        description = endpoints[endpoint]
        if description != ' ':
            description = '[More information](%s)' % description

        obs_count = 0
        start_year = end_year

        def create_resource():
            urllist[-1] = '&startPeriod=%d&endPeriod=%d' % (start_year, end_year)
            resource = {
                'name': '%s (%d-%d)' % (indicator, start_year, end_year),
                'description': description,
                'format': 'csv',
                'url': downloader.get_full_url(''.join(urllist))
            }
            dataset.add_update_resource(resource)

        for year in years:
            obs_count += time_periods[year]
            if obs_count < 2000:
                start_year = year
                continue
            obs_count = time_periods[year]
            create_resource()
            end_year = year
        create_resource()
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
