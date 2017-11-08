#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Unit tests for scrapername.

'''
from os.path import join
from pprint import pprint

import pytest
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations
from hdx.location.country import Country

from unesco import generate_dataset_and_showcase, get_countriesdata


class TestUnesco:
    countrydata = {'urn': 'urn:sdmx:org.sdmx.infomodel.codelist.Code=UNESCO:CL_AREA(1.0).AR', 'id': 'AR', 'names': [{'value': 'Argentina', 'locale': 'en'}]}
    dimensions = [{'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS(1.0).STAT_UNIT', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).STAT_UNIT', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_STAT_UNIT(1.0)'}, 'id': 'STAT_UNIT'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS(1.0).UNIT_MEASURE', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).UNIT_MEASURE', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_UNIT(1.0)'}, 'id': 'UNIT_MEASURE'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).EDU_LEVEL', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).EDU_LEVEL', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_EDU_LEVEL(1.0)'}, 'id': 'EDU_LEVEL'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).EDU_CAT', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).EDU_CAT', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_EDU_CAT(1.0)'}, 'id': 'EDU_CAT'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).SECTOR_EDU', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).SECTOR_EDU', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_SECTOR_EDU(1.0)'}, 'id': 'SECTOR_EDU'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).EXPENDITURE_TYPE', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).EXPENDITURE_TYPE', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_EXPENDITURE_TYPE(1.0)'}, 'id': 'EXPENDITURE_TYPE'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).SOURCE_FUND', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).SOURCE_FUND', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_SOURCE_FUND(1.0)'}, 'id': 'SOURCE_FUND'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).FUND_FLOW', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).FUND_FLOW', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_FUND_FLOW(1.0)'}, 'id': 'FUND_FLOW'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).TEACH_EXPERIENCE', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).TEACH_EXPERIENCE', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_TEACH_EXPERIENCE(1.0)'}, 'id': 'TEACH_EXPERIENCE'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=UNESCO:EDU(1.0).CONTRACT_TYPE', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).CONTRACT_TYPE', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_CONTRACT_TYPE(1.0)'}, 'id': 'CONTRACT_TYPE'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS(1.0).REF_AREA', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.Dimension=UNESCO:EDU_FINANCE(1.0).REF_AREA', 'representation': {'representation': 'urn:sdmx:org.sdmx.infomodel.codelist.Codelist=UNESCO:CL_AREA(1.0)'}, 'id': 'REF_AREA'}, {'concept': 'urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS(1.0).TIME_PERIOD', 'urn': 'urn:sdmx:org.sdmx.infomodel.datastructure.TimeDimension=UNESCO:EDU_FINANCE(1.0).TIME_PERIOD', 'isTimeDimension': True, 'representation': {}, 'id': 'TIME_PERIOD'}]
    observations = [{'maxObs': 2488320, 'name': 'Statistical unit', 'id': 'STAT_UNIT', 'role': None, 'keyPosition': 1, 'values': [{'inDataset': True, 'actualObs': 2151, 'name': 'Government expenditure per student', 'id': 'XUNIT'}, {'inDataset': True, 'actualObs': 4034, 'name': 'Expenditure on education', 'id': 'EDU_EXP'}]}, {'maxObs': 414720, 'name': 'Unit of measure', 'id': 'UNIT_MEASURE', 'role': None, 'keyPosition': 2, 'values': [{'inDataset': True, 'actualObs': 584, 'name': 'Constant PPP $', 'id': 'PPP_CONST'}, {'inDataset': True, 'actualObs': 176, 'name': 'as % of total government expenditure (all sectors)', 'id': 'GOV_EXP_T'}, {'inDataset': True, 'actualObs': 136, 'name': 'as % of GNI per capita', 'id': 'GNI_CAP'}, {'inDataset': True, 'actualObs': 584, 'name': 'Purchasing power parity', 'id': 'PPP'}, {'inDataset': True, 'actualObs': 403, 'name': 'as % of GDP per capita', 'id': 'GDP_CAP'}, {'inDataset': True, 'actualObs': 800, 'name': 'as % of GDP', 'id': 'GDP'}, {'inDataset': True, 'actualObs': 638, 'name': 'as a % of total current expenditure on education', 'id': 'CUR_EXP'}, {'inDataset': True, 'actualObs': 427, 'name': 'as % of total government expenditure on education', 'id': 'GOV_EXP_EDU'}, {'inDataset': True, 'actualObs': 392, 'name': 'as % of GNI', 'id': 'GNI'}, {'inDataset': True, 'actualObs': 669, 'name': 'US dollar', 'id': 'USD'}, {'inDataset': True, 'actualObs': 707, 'name': 'as % of total expenditure', 'id': 'EXP_T'}, {'inDataset': True, 'actualObs': 669, 'name': 'Constant US $', 'id': 'USD_CONST'}]}, {'maxObs': 497664, 'name': 'Level of education', 'id': 'EDU_LEVEL', 'role': None, 'keyPosition': 3, 'values': [{'inDataset': True, 'actualObs': 506, 'name': 'Total', 'id': '_T'}, {'inDataset': True, 'actualObs': 943, 'name': 'Primary education', 'id': 'L1'}, {'inDataset': True, 'actualObs': 625, 'name': 'Lower secondary education', 'id': 'L2'}, {'inDataset': True, 'actualObs': 625, 'name': 'Upper secondary education', 'id': 'L3'}, {'inDataset': True, 'actualObs': 36, 'name': 'Pre-primary education to secondary education', 'id': 'L02T3'}, {'inDataset': True, 'actualObs': 567, 'name': 'Post-secondary non-tertiary education', 'id': 'L4'}, {'inDataset': True, 'actualObs': 873, 'name': 'Secondary education', 'id': 'L2_3'}, {'inDataset': True, 'actualObs': 193, 'name': 'Not allocated by level', 'id': '_X'}, {'inDataset': True, 'actualObs': 822, 'name': 'Tertiary education', 'id': 'L5T8'}, {'inDataset': True, 'actualObs': 995, 'name': 'Pre-primary education', 'id': 'L02'}]}, {'maxObs': 4976640, 'name': 'Orientation', 'id': 'EDU_CAT', 'role': None, 'keyPosition': 4, 'values': [{'inDataset': True, 'actualObs': 6185, 'name': 'Total', 'id': '_T'}]}, {'maxObs': 1658880, 'name': 'Type of institution', 'id': 'SECTOR_EDU', 'role': None, 'keyPosition': 5, 'values': [{'inDataset': True, 'actualObs': 4895, 'name': 'Total', 'id': '_T'}, {'inDataset': True, 'actualObs': 90, 'name': 'All institutions', 'id': 'INST_T'}, {'inDataset': True, 'actualObs': 1200, 'name': 'Public institutions', 'id': 'INST_PUB'}]}, {'maxObs': 622080, 'name': 'Type of expenditure', 'id': 'EXPENDITURE_TYPE', 'role': None, 'keyPosition': 6, 'values': [{'inDataset': True, 'actualObs': 1130, 'name': 'Current', 'id': 'CUR'}, {'inDataset': True, 'actualObs': 117, 'name': 'Capital', 'id': 'CAP'}, {'inDataset': True, 'actualObs': 161, 'name': 'Current and transfer expenditure', 'id': 'CUR_TRF'}, {'inDataset': True, 'actualObs': 3812, 'name': 'Total', 'id': '_T'}, {'inDataset': True, 'actualObs': 242, 'name': 'Expenditure for compensation of personnel', 'id': 'CUR_COMP'}, {'inDataset': True, 'actualObs': 237, 'name': 'Current expenditure other than for compensation of personnel', 'id': 'CUR_O'}, {'inDataset': True, 'actualObs': 242, 'name': 'Expenditure for compensation of teaching staff', 'id': 'CUR_COMPT'}, {'inDataset': True, 'actualObs': 244, 'name': 'Expenditure for compensation of non-teaching staff', 'id': 'CUR_COMPO'}]}, {'maxObs': 2488320, 'name': 'Source of funding', 'id': 'SOURCE_FUND', 'role': None, 'keyPosition': 7, 'values': [{'inDataset': True, 'actualObs': 299, 'name': 'Household', 'id': 'HH'}, {'inDataset': True, 'actualObs': 5886, 'name': 'Government', 'id': 'GOV'}]}, {'maxObs': 1658880, 'name': 'Funding flow', 'id': 'FUND_FLOW', 'role': None, 'keyPosition': 8, 'values': [{'inDataset': True, 'actualObs': 2561, 'name': 'Final (net of transfers paid)', 'id': 'FFNTP'}, {'inDataset': True, 'actualObs': 2568, 'name': 'Total (include transfers paid and received)', 'id': '_T'}, {'inDataset': True, 'actualObs': 1056, 'name': 'Initial (net of transfers received)', 'id': 'FFNTR'}]}, {'maxObs': 2488320, 'name': 'Teaching experience', 'id': 'TEACH_EXPERIENCE', 'role': None, 'keyPosition': 9, 'values': [{'inDataset': True, 'actualObs': 242, 'name': 'Total', 'id': '_T'}, {'inDataset': True, 'actualObs': 5943, 'name': 'Not applicable', 'id': '_Z'}]}, {'maxObs': 2488320, 'name': 'Type of contract', 'id': 'CONTRACT_TYPE', 'role': None, 'keyPosition': 10, 'values': [{'inDataset': True, 'actualObs': 242, 'name': 'Total', 'id': '_T'}, {'inDataset': True, 'actualObs': 5943, 'name': 'Not applicable', 'id': '_Z'}]}, {'maxObs': 138568320, 'name': 'Reference area', 'id': 'REF_AREA', 'role': None, 'keyPosition': 11, 'values': [{'inDataset': False, 'actualObs': 625, 'name': 'Puerto Rico', 'id': 'PR'}, {'inDataset': False, 'actualObs': 97, 'name': 'Palestine', 'id': 'PS'}, {'inDataset': False, 'actualObs': 5758, 'name': 'Portugal', 'id': 'PT'}, {'inDataset': False, 'actualObs': 122, 'name': 'Palau', 'id': 'PW'}, {'inDataset': False, 'actualObs': 2791, 'name': 'Paraguay', 'id': 'PY'}, {'inDataset': False, 'actualObs': 548, 'name': 'Qatar', 'id': 'QA'}, {'inDataset': False, 'actualObs': 1988, 'name': 'Andorra', 'id': 'AD'}, {'inDataset': False, 'actualObs': 488, 'name': 'United Arab Emirates', 'id': 'AE'}, {'inDataset': False, 'actualObs': 1987, 'name': 'Afghanistan', 'id': 'AF'}, {'inDataset': False, 'actualObs': 534, 'name': 'Antigua and Barbuda', 'id': 'AG'}, {'inDataset': False, 'actualObs': 396, 'name': 'Anguilla', 'id': 'AI'}, {'inDataset': False, 'actualObs': 355, 'name': 'Albania', 'id': 'AL'}, {'inDataset': False, 'actualObs': 1271, 'name': 'Armenia', 'id': 'AM'}, {'inDataset': False, 'actualObs': 364, 'name': 'Angola', 'id': 'AO'}, {'inDataset': True, 'actualObs': 6185, 'name': 'Argentina', 'id': 'AR'}, {'inDataset': False, 'actualObs': 6369, 'name': 'Austria', 'id': 'AT'}, {'inDataset': False, 'actualObs': 4164, 'name': 'Australia', 'id': 'AU'}, {'inDataset': False, 'actualObs': 1522, 'name': 'Aruba', 'id': 'AW'}, {'inDataset': False, 'actualObs': 1603, 'name': 'Azerbaijan', 'id': 'AZ'}, {'inDataset': False, 'actualObs': 3301, 'name': 'Romania', 'id': 'RO'}, {'inDataset': False, 'actualObs': 2725, 'name': 'Barbados', 'id': 'BB'}, {'inDataset': False, 'actualObs': 1290, 'name': 'Serbia', 'id': 'RS'}, {'inDataset': False, 'actualObs': 3251, 'name': 'Bangladesh', 'id': 'BD'}, {'inDataset': False, 'actualObs': 3425, 'name': 'Belgium', 'id': 'BE'}, {'inDataset': False, 'actualObs': 624, 'name': 'Russian Federation', 'id': 'RU'}, {'inDataset': False, 'actualObs': 2520, 'name': 'Burkina Faso', 'id': 'BF'}, {'inDataset': False, 'actualObs': 2393, 'name': 'Rwanda', 'id': 'RW'}, {'inDataset': False, 'actualObs': 4559, 'name': 'Bulgaria', 'id': 'BG'}, {'inDataset': False, 'actualObs': 739, 'name': 'Bahrain', 'id': 'BH'}, {'inDataset': False, 'actualObs': 2658, 'name': 'Burundi', 'id': 'BI'}, {'inDataset': False, 'actualObs': 2753, 'name': 'Benin', 'id': 'BJ'}, {'inDataset': False, 'actualObs': 1144, 'name': 'Bermuda', 'id': 'BM'}, {'inDataset': False, 'actualObs': 1382, 'name': 'Brunei Darussalam', 'id': 'BN'}, {'inDataset': False, 'actualObs': 3187, 'name': 'Bolivia (Plurinational State of)', 'id': 'BO'}, {'inDataset': False, 'actualObs': 401, 'name': 'Saudi Arabia', 'id': 'SA'}, {'inDataset': False, 'actualObs': 124, 'name': 'Solomon Islands', 'id': 'SB'}, {'inDataset': False, 'actualObs': 3695, 'name': 'Brazil', 'id': 'BR'}, {'inDataset': False, 'actualObs': 1633, 'name': 'Seychelles', 'id': 'SC'}, {'inDataset': False, 'actualObs': 78, 'name': 'Sudan', 'id': 'SD'}, {'inDataset': False, 'actualObs': 8, 'name': 'Bahamas', 'id': 'BS'}, {'inDataset': False, 'actualObs': 5036, 'name': 'Sweden', 'id': 'SE'}, {'inDataset': False, 'actualObs': 1644, 'name': 'Bhutan', 'id': 'BT'}, {'inDataset': False, 'actualObs': 1550, 'name': 'Singapore', 'id': 'SG'}, {'inDataset': False, 'actualObs': 1374, 'name': 'Botswana', 'id': 'BW'}, {'inDataset': False, 'actualObs': 2839, 'name': 'Slovenia', 'id': 'SI'}, {'inDataset': False, 'actualObs': 1291, 'name': 'Belarus', 'id': 'BY'}, {'inDataset': False, 'actualObs': 5293, 'name': 'Slovakia', 'id': 'SK'}, {'inDataset': False, 'actualObs': 1930, 'name': 'Belize', 'id': 'BZ'}, {'inDataset': False, 'actualObs': 1660, 'name': 'Sierra Leone', 'id': 'SL'}, {'inDataset': False, 'actualObs': 675, 'name': 'San Marino', 'id': 'SM'}, {'inDataset': False, 'actualObs': 2187, 'name': 'Senegal', 'id': 'SN'}, {'inDataset': False, 'actualObs': 54, 'name': 'Somalia', 'id': 'SO'}, {'inDataset': False, 'actualObs': 1353, 'name': 'Canada', 'id': 'CA'}, {'inDataset': False, 'actualObs': 926, 'name': 'South Sudan', 'id': 'SS'}, {'inDataset': False, 'actualObs': 1015, 'name': 'Sao Tome and Principe', 'id': 'ST'}, {'inDataset': False, 'actualObs': 933, 'name': 'Democratic Republic of the Congo', 'id': 'CD'}, {'inDataset': False, 'actualObs': 1398, 'name': 'Central African Republic', 'id': 'CF'}, {'inDataset': False, 'actualObs': 3783, 'name': 'El Salvador', 'id': 'SV'}, {'inDataset': False, 'actualObs': 932, 'name': 'Congo', 'id': 'CG'}, {'inDataset': False, 'actualObs': 5580, 'name': 'Switzerland', 'id': 'CH'}, {'inDataset': False, 'actualObs': 3978, 'name': "Côte d'Ivoire", 'id': 'CI'}, {'inDataset': False, 'actualObs': 1799, 'name': 'Syrian Arab Republic', 'id': 'SY'}, {'inDataset': False, 'actualObs': 2318, 'name': 'Swaziland', 'id': 'SZ'}, {'inDataset': False, 'actualObs': 546, 'name': 'Cook Islands', 'id': 'CK'}, {'inDataset': False, 'actualObs': 5087, 'name': 'Chile', 'id': 'CL'}, {'inDataset': False, 'actualObs': 2293, 'name': 'Cameroon', 'id': 'CM'}, {'inDataset': False, 'actualObs': 1212, 'name': 'China', 'id': 'CN'}, {'inDataset': False, 'actualObs': 4206, 'name': 'Colombia', 'id': 'CO'}, {'inDataset': False, 'actualObs': 3932, 'name': 'Costa Rica', 'id': 'CR'}, {'inDataset': False, 'actualObs': 759, 'name': 'Turks and Caicos Islands', 'id': 'TC'}, {'inDataset': False, 'actualObs': 1741, 'name': 'Chad', 'id': 'TD'}, {'inDataset': False, 'actualObs': 2517, 'name': 'Cuba', 'id': 'CU'}, {'inDataset': False, 'actualObs': 1513, 'name': 'Cabo Verde', 'id': 'CV'}, {'inDataset': False, 'actualObs': 3612, 'name': 'Togo', 'id': 'TG'}, {'inDataset': False, 'actualObs': 129, 'name': 'Curaçao', 'id': 'CW'}, {'inDataset': False, 'actualObs': 2899, 'name': 'Thailand', 'id': 'TH'}, {'inDataset': False, 'actualObs': 5468, 'name': 'Cyprus', 'id': 'CY'}, {'inDataset': False, 'actualObs': 1281, 'name': 'Tajikistan', 'id': 'TJ'}, {'inDataset': False, 'actualObs': 43, 'name': 'Tokelau', 'id': 'TK'}, {'inDataset': False, 'actualObs': 5315, 'name': 'Czechia', 'id': 'CZ'}, {'inDataset': False, 'actualObs': 1277, 'name': 'Timor-Leste', 'id': 'TL'}, {'inDataset': False, 'actualObs': 50, 'name': 'Turkmenistan', 'id': 'TM'}, {'inDataset': False, 'actualObs': 2689, 'name': 'Tunisia', 'id': 'TN'}, {'inDataset': False, 'actualObs': 492, 'name': 'Tonga', 'id': 'TO'}, {'inDataset': False, 'actualObs': 2581, 'name': 'Turkey', 'id': 'TR'}, {'inDataset': False, 'actualObs': 874, 'name': 'Trinidad and Tobago', 'id': 'TT'}, {'inDataset': False, 'actualObs': 2638, 'name': 'Germany', 'id': 'DE'}, {'inDataset': False, 'actualObs': 70, 'name': 'Tuvalu', 'id': 'TV'}, {'inDataset': False, 'actualObs': 741, 'name': 'Djibouti', 'id': 'DJ'}, {'inDataset': False, 'actualObs': 1098, 'name': 'United Republic of Tanzania', 'id': 'TZ'}, {'inDataset': False, 'actualObs': 5514, 'name': 'Denmark', 'id': 'DK'}, {'inDataset': False, 'actualObs': 1063, 'name': 'Dominica', 'id': 'DM'}, {'inDataset': False, 'actualObs': 3137, 'name': 'Dominican Republic', 'id': 'DO'}, {'inDataset': False, 'actualObs': 1373, 'name': 'Ukraine', 'id': 'UA'}, {'inDataset': False, 'actualObs': 2100, 'name': 'Uganda', 'id': 'UG'}, {'inDataset': False, 'actualObs': 682, 'name': 'Algeria', 'id': 'DZ'}, {'inDataset': False, 'actualObs': 2432, 'name': 'Ecuador', 'id': 'EC'}, {'inDataset': False, 'actualObs': 4456, 'name': 'United States of America', 'id': 'US'}, {'inDataset': False, 'actualObs': 3761, 'name': 'Estonia', 'id': 'EE'}, {'inDataset': False, 'actualObs': 442, 'name': 'Egypt', 'id': 'EG'}, {'inDataset': False, 'actualObs': 2703, 'name': 'Uruguay', 'id': 'UY'}, {'inDataset': False, 'actualObs': 1759, 'name': 'Saint Vincent and the Grenadines', 'id': 'VC'}, {'inDataset': False, 'actualObs': 601, 'name': 'Eritrea', 'id': 'ER'}, {'inDataset': False, 'actualObs': 5018, 'name': 'Spain', 'id': 'ES'}, {'inDataset': False, 'actualObs': 1458, 'name': 'Venezuela (Bolivarian Republic of)', 'id': 'VE'}, {'inDataset': False, 'actualObs': 1864, 'name': 'Ethiopia', 'id': 'ET'}, {'inDataset': False, 'actualObs': 691, 'name': 'British Virgin Islands', 'id': 'VG'}, {'inDataset': False, 'actualObs': 1375, 'name': 'Viet Nam', 'id': 'VN'}, {'inDataset': False, 'actualObs': 1616, 'name': 'Vanuatu', 'id': 'VU'}, {'inDataset': False, 'actualObs': 5651, 'name': 'Finland', 'id': 'FI'}, {'inDataset': False, 'actualObs': 676, 'name': 'Fiji', 'id': 'FJ'}, {'inDataset': False, 'actualObs': 53, 'name': 'Micronesia (Federated States of)', 'id': 'FM'}, {'inDataset': False, 'actualObs': 5930, 'name': 'France', 'id': 'FR'}, {'inDataset': False, 'actualObs': 1018, 'name': 'Gabon', 'id': 'GA'}, {'inDataset': False, 'actualObs': 5509, 'name': 'United Kingdom of Great Britain and Northern Ireland', 'id': 'GB'}, {'inDataset': False, 'actualObs': 647, 'name': 'Samoa', 'id': 'WS'}, {'inDataset': False, 'actualObs': 213, 'name': 'Grenada', 'id': 'GD'}, {'inDataset': False, 'actualObs': 602, 'name': 'Georgia', 'id': 'GE'}, {'inDataset': False, 'actualObs': 3899, 'name': 'Ghana', 'id': 'GH'}, {'inDataset': False, 'actualObs': 2881, 'name': 'Gambia', 'id': 'GM'}, {'inDataset': False, 'actualObs': 2133, 'name': 'Guinea', 'id': 'GN'}, {'inDataset': False, 'actualObs': 62, 'name': 'Equatorial Guinea', 'id': 'GQ'}, {'inDataset': False, 'actualObs': 1755, 'name': 'Greece', 'id': 'GR'}, {'inDataset': False, 'actualObs': 3400, 'name': 'Guatemala', 'id': 'GT'}, {'inDataset': False, 'actualObs': 863, 'name': 'Guinea-Bissau', 'id': 'GW'}, {'inDataset': False, 'actualObs': 2089, 'name': 'Guyana', 'id': 'GY'}, {'inDataset': False, 'actualObs': 3068, 'name': 'China, Hong Kong Special Administrative Region', 'id': 'HK'}, {'inDataset': False, 'actualObs': 1007, 'name': 'Honduras', 'id': 'HN'}, {'inDataset': False, 'actualObs': 1510, 'name': 'Croatia', 'id': 'HR'}, {'inDataset': False, 'actualObs': 237, 'name': 'Yemen', 'id': 'YE'}, {'inDataset': False, 'actualObs': 125, 'name': 'Haiti', 'id': 'HT'}, {'inDataset': False, 'actualObs': 4922, 'name': 'Hungary', 'id': 'HU'}, {'inDataset': False, 'actualObs': 2671, 'name': 'Indonesia', 'id': 'ID'}, {'inDataset': False, 'actualObs': 5986, 'name': 'Ireland', 'id': 'IE'}, {'inDataset': False, 'actualObs': 4598, 'name': 'Israel', 'id': 'IL'}, {'inDataset': False, 'actualObs': 2486, 'name': 'India', 'id': 'IN'}, {'inDataset': False, 'actualObs': 2857, 'name': 'South Africa', 'id': 'ZA'}, {'inDataset': False, 'actualObs': 140, 'name': 'Iraq', 'id': 'IQ'}, {'inDataset': False, 'actualObs': 4327, 'name': 'Iran (Islamic Republic of)', 'id': 'IR'}, {'inDataset': False, 'actualObs': 4265, 'name': 'Iceland', 'id': 'IS'}, {'inDataset': False, 'actualObs': 5952, 'name': 'Italy', 'id': 'IT'}, {'inDataset': False, 'actualObs': 1730, 'name': 'Zambia', 'id': 'ZM'}, {'inDataset': False, 'actualObs': 1430, 'name': 'Zimbabwe', 'id': 'ZW'}, {'inDataset': False, 'actualObs': 4294, 'name': 'Jamaica', 'id': 'JM'}, {'inDataset': False, 'actualObs': 2823, 'name': 'Jordan', 'id': 'JO'}, {'inDataset': False, 'actualObs': 4095, 'name': 'Japan', 'id': 'JP'}, {'inDataset': False, 'actualObs': 2956, 'name': 'Kenya', 'id': 'KE'}, {'inDataset': False, 'actualObs': 1914, 'name': 'Kyrgyzstan', 'id': 'KG'}, {'inDataset': False, 'actualObs': 1681, 'name': 'Cambodia', 'id': 'KH'}, {'inDataset': False, 'actualObs': 194, 'name': 'Kiribati', 'id': 'KI'}, {'inDataset': False, 'actualObs': 1373, 'name': 'Comoros', 'id': 'KM'}, {'inDataset': False, 'actualObs': 806, 'name': 'Saint Kitts and Nevis', 'id': 'KN'}, {'inDataset': False, 'actualObs': 5263, 'name': 'Republic of Korea', 'id': 'KR'}, {'inDataset': False, 'actualObs': 2543, 'name': 'Kuwait', 'id': 'KW'}, {'inDataset': False, 'actualObs': 160, 'name': 'Cayman Islands', 'id': 'KY'}, {'inDataset': False, 'actualObs': 1373, 'name': 'Kazakhstan', 'id': 'KZ'}, {'inDataset': False, 'actualObs': 2547, 'name': "Lao People's Democratic Republic", 'id': 'LA'}, {'inDataset': False, 'actualObs': 1711, 'name': 'Lebanon', 'id': 'LB'}, {'inDataset': False, 'actualObs': 2107, 'name': 'Saint Lucia', 'id': 'LC'}, {'inDataset': False, 'actualObs': 1006, 'name': 'Liechtenstein', 'id': 'LI'}, {'inDataset': False, 'actualObs': 2487, 'name': 'Sri Lanka', 'id': 'LK'}, {'inDataset': False, 'actualObs': 219, 'name': 'Liberia', 'id': 'LR'}, {'inDataset': False, 'actualObs': 1565, 'name': 'Lesotho', 'id': 'LS'}, {'inDataset': False, 'actualObs': 3508, 'name': 'Lithuania', 'id': 'LT'}, {'inDataset': False, 'actualObs': 3317, 'name': 'Luxembourg', 'id': 'LU'}, {'inDataset': False, 'actualObs': 3817, 'name': 'Latvia', 'id': 'LV'}, {'inDataset': False, 'actualObs': 80, 'name': 'Libya', 'id': 'LY'}, {'inDataset': False, 'actualObs': 3515, 'name': 'Morocco', 'id': 'MA'}, {'inDataset': False, 'actualObs': 2141, 'name': 'Monaco', 'id': 'MC'}, {'inDataset': False, 'actualObs': 2619, 'name': 'Republic of Moldova', 'id': 'MD'}, {'inDataset': False, 'actualObs': 2506, 'name': 'Madagascar', 'id': 'MG'}, {'inDataset': False, 'actualObs': 332, 'name': 'Marshall Islands', 'id': 'MH'}, {'inDataset': False, 'actualObs': 399, 'name': 'The former Yugoslav Republic of Macedonia', 'id': 'MK'}, {'inDataset': False, 'actualObs': 2619, 'name': 'Mali', 'id': 'ML'}, {'inDataset': False, 'actualObs': 238, 'name': 'Myanmar', 'id': 'MM'}, {'inDataset': False, 'actualObs': 1331, 'name': 'Mongolia', 'id': 'MN'}, {'inDataset': False, 'actualObs': 1490, 'name': 'China, Macao Special Administrative Region', 'id': 'MO'}, {'inDataset': False, 'actualObs': 1017, 'name': 'Mauritania', 'id': 'MR'}, {'inDataset': False, 'actualObs': 246, 'name': 'Montserrat', 'id': 'MS'}, {'inDataset': False, 'actualObs': 4089, 'name': 'Malta', 'id': 'MT'}, {'inDataset': False, 'actualObs': 2671, 'name': 'Mauritius', 'id': 'MU'}, {'inDataset': False, 'actualObs': 2053, 'name': 'Maldives', 'id': 'MV'}, {'inDataset': False, 'actualObs': 2440, 'name': 'Malawi', 'id': 'MW'}, {'inDataset': False, 'actualObs': 5158, 'name': 'Mexico', 'id': 'MX'}, {'inDataset': False, 'actualObs': 4144, 'name': 'Malaysia', 'id': 'MY'}, {'inDataset': False, 'actualObs': 917, 'name': 'Mozambique', 'id': 'MZ'}, {'inDataset': False, 'actualObs': 1219, 'name': 'Namibia', 'id': 'NA'}, {'inDataset': False, 'actualObs': 2715, 'name': 'Niger', 'id': 'NE'}, {'inDataset': False, 'actualObs': 95, 'name': 'Nigeria', 'id': 'NG'}, {'inDataset': False, 'actualObs': 1206, 'name': 'Nicaragua', 'id': 'NI'}, {'inDataset': False, 'actualObs': 4982, 'name': 'Netherlands', 'id': 'NL'}, {'inDataset': False, 'actualObs': 4772, 'name': 'Norway', 'id': 'NO'}, {'inDataset': False, 'actualObs': 3470, 'name': 'Nepal', 'id': 'NP'}, {'inDataset': False, 'actualObs': 3, 'name': 'Nauru', 'id': 'NR'}, {'inDataset': False, 'actualObs': 113, 'name': 'Niue', 'id': 'NU'}, {'inDataset': False, 'actualObs': 4622, 'name': 'New Zealand', 'id': 'NZ'}, {'inDataset': False, 'actualObs': 2603, 'name': 'Oman', 'id': 'OM'}, {'inDataset': False, 'actualObs': 2159, 'name': 'Panama', 'id': 'PA'}, {'inDataset': False, 'actualObs': 4053, 'name': 'Peru', 'id': 'PE'}, {'inDataset': False, 'actualObs': 92, 'name': 'Papua New Guinea', 'id': 'PG'}, {'inDataset': False, 'actualObs': 2913, 'name': 'Philippines', 'id': 'PH'}, {'inDataset': False, 'actualObs': 1747, 'name': 'Pakistan', 'id': 'PK'}, {'inDataset': False, 'actualObs': 4367, 'name': 'Poland', 'id': 'PL'}]}, {'maxObs': 325, 'name': 'Time period', 'id': 'TIME_PERIOD', 'role': 'time', 'keyPosition': 12,
                     'values': [{'inDataset': True, 'actualObs': 325, 'name': '2014', 'id': '2014'}, {'inDataset': True, 'actualObs': 325, 'name': '2013', 'id': '2013'}, {'inDataset': True, 'actualObs': 306, 'name': '2012', 'id': '2012'}, {'inDataset': True, 'actualObs': 305, 'name': '2011', 'id': '2011'}, {'inDataset': True, 'actualObs': 325, 'name': '2010', 'id': '2010'}, {'inDataset': True, 'actualObs': 325, 'name': '2009', 'id': '2009'}, {'inDataset': True, 'actualObs': 325, 'name': '2008', 'id': '2008'}, {'inDataset': True, 'actualObs': 325, 'name': '2007', 'id': '2007'}, {'inDataset': True, 'actualObs': 325, 'name': '2006', 'id': '2006'}, {'inDataset': True, 'actualObs': 286, 'name': '2005', 'id': '2005'}, {'inDataset': True, 'actualObs': 325, 'name': '2004', 'id': '2004'}, {'inDataset': True, 'actualObs': 325, 'name': '2003', 'id': '2003'}, {'inDataset': True, 'actualObs': 325, 'name': '2002', 'id': '2002'}, {'inDataset': True, 'actualObs': 302, 'name': '2001', 'id': '2001'}, {'inDataset': True, 'actualObs': 229, 'name': '2000', 'id': '2000'}, {'inDataset': True, 'actualObs': 207, 'name': '1999', 'id': '1999'}, {'inDataset': True, 'actualObs': 259, 'name': '1998', 'id': '1998'}, {'inDataset': True, 'actualObs': 59, 'name': '1996', 'id': '1996'}, {'inDataset': True, 'actualObs': 65, 'name': '1990', 'id': '1990'}, {'inDataset': True, 'actualObs': 55, 'name': '1989', 'id': '1989'}, {'inDataset': True, 'actualObs': 55, 'name': '1987', 'id': '1987'}, {'inDataset': True, 'actualObs': 55, 'name': '1986', 'id': '1986'}, {'inDataset': True, 'actualObs': 55, 'name': '1985', 'id': '1985'}, {'inDataset': True, 'actualObs': 55, 'name': '1984', 'id': '1984'}, {'inDataset': True, 'actualObs': 55, 'name': '1983', 'id': '1983'}, {'inDataset': True, 'actualObs': 55, 'name': '1982', 'id': '1982'}, {'inDataset': True, 'actualObs': 55, 'name': '1980', 'id': '1980'}, {'inDataset': True, 'actualObs': 55, 'name': '1979', 'id': '1979'}, {'inDataset': True, 'actualObs': 55, 'name': '1978', 'id': '1978'}, {'inDataset': True, 'actualObs': 55, 'name': '1977', 'id': '1977'}, {'inDataset': True, 'actualObs': 55, 'name': '1976', 'id': '1976'}, {'inDataset': True, 'actualObs': 55, 'name': '1975', 'id': '1975'}, {'inDataset': True, 'actualObs': 55, 'name': '1974', 'id': '1974'}, {'inDataset': True, 'actualObs': 55, 'name': '1973', 'id': '1973'}, {'inDataset': True, 'actualObs': 55, 'name': '1972', 'id': '1972'}, {'inDataset': True, 'actualObs': 37, 'name': '1970', 'id': '1970'}]}]

    @pytest.fixture(scope='function')
    def configuration(self):
        Configuration._create(hdx_read_only=True,
                              project_config_yaml=join('tests', 'config', 'project_configuration.yml'))
        Locations.set_validlocations([{'name': 'arg', 'title': 'Argentina'}])  # add locations used in tests
        Country.countriesdata(use_live=False)

    @pytest.fixture(scope='function')
    def downloader(self):
        class Response:
            @staticmethod
            def json():
                pass

        class Download:
            @staticmethod
            def download(url):
                response = Response()
                if url == 'http://xxx/codelist/UNESCO/CL_AREA/latest?format=sdmx-json':
                    def fn():
                        return {'Codelist': [{'items': [TestUnesco.countrydata]}]}
                    response.json = fn
                elif url == 'http://yyyy/dataflow/UNESCO/EDU_FINANCE/latest?references=datastructure&format=sdmx-json':
                    def fn():
                        return {'Dataflow': [{'names': [{'value': 'Education: Financial resources'}]}],
                                'DataStructure': [{'dimensionList': {'dimensions': TestUnesco.dimensions}}]}
                    response.json = fn
                elif url == 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=sdmx-json&detail=structureonly&includeMetrics=true':
                    def fn():
                        return {'structure': {'dimensions': {'observation': TestUnesco.observations}}}
                    response.json = fn
                return response

            @staticmethod
            def get_full_url(url):
                url_prefix = 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=csv'
                if url[:len(url_prefix)] == url_prefix:
                    return '%s&locale=en&subscription-key=12345' % url

        return Download()

    def test_get_countriesdata(self, downloader):
        countriesdata = get_countriesdata('http://xxx/', downloader)
        assert countriesdata == [TestUnesco.countrydata]

    def test_generate_dataset_and_showcase(self, configuration, downloader):
        dataset, showcase = generate_dataset_and_showcase('http://yyyy/', downloader, TestUnesco.countrydata,
                                                          {'EDU_FINANCE': 'http://uis.unesco.org/en/topic/education-finance'})
        assert dataset == {'tags': [{'name': 'indicators'}, {'name': 'UNESCO'}, {'name': 'sustainable development'},
                                    {'name': 'demographic'}, {'name': 'socioeconomic'}, {'name': 'education'}],
                           'owner_org': '18f2d467-dcf8-4b7e-bffa-b3c338ba3a7c', 'data_update_frequency': '365',
                           'title': 'Argentina - Sustainable development, Education, Demographic and Socioeconomic Indicators',
                           'groups': [{'name': 'arg'}], 'maintainer': '196196be-6037-4488-8b71-d786adf4c081',
                           'name': 'unesco-indicators-for-argentina', 'dataset_date': '01/01/1970-12/31/2014'}
        resources = dataset.get_resources()
        pprint(TestUnesco.observations)

        assert resources == [{'description': '[More information](http://uis.unesco.org/en/topic/education-finance)',
                              'url': 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=csv&startPeriod=2009&endPeriod=2014&locale=en&subscription-key=12345',
                              'name': 'Education: Financial resources (2009-2014)', 'format': 'csv'},
                             {'description': '[More information](http://uis.unesco.org/en/topic/education-finance)',
                              'url': 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=csv&startPeriod=2003&endPeriod=2008&locale=en&subscription-key=12345',
                              'name': 'Education: Financial resources (2003-2008)', 'format': 'csv'},
                             {'description': '[More information](http://uis.unesco.org/en/topic/education-finance)',
                              'url': 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=csv&startPeriod=1978&endPeriod=2002&locale=en&subscription-key=12345',
                              'name': 'Education: Financial resources (1978-2002)', 'format': 'csv'},
                             {'description': '[More information](http://uis.unesco.org/en/topic/education-finance)',
                              'url': 'http://yyyy/data/UNESCO,EDU_FINANCE,1.0/..........AR.?format=csv&startPeriod=1970&endPeriod=1977&locale=en&subscription-key=12345',
                              'name': 'Education: Financial resources (1970-1977)', 'format': 'csv'}]

        assert showcase == {'name': 'unesco-indicators-for-argentina-showcase',
                            'notes': 'Education, literacy and other indicators for Argentina',
                            'image_url': 'http://www.tellmaps.com/uis/internal/assets/uisheader-en.png',
                            'url': 'http://uis.unesco.org/en/country/AR',
                            'tags': [{'name': 'indicators'}, {'name': 'UNESCO'}, {'name': 'sustainable development'},
                                     {'name': 'demographic'}, {'name': 'socioeconomic'}, {'name': 'education'}],
                            'title': 'Indicators for Argentina'}

