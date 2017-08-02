#!/usr/bin/env python3

"""
main_retrieve_ei.py:
    Master script to download ERA-Interim data.

Usage:
    ./main_retrieve_ei.py

Author:
    Benjamin S. Grandey, 2017
"""

from ecmwf_data import retrieve_era_interim


# Region bounds (N/W/S/E)
area = '30/60/-20/150'  # Southeast Asia, agreed with Hsiang-He

# Years to retrieve
years = [str(y) for y in range(1979, 2016+1)]  # 1979-2016

# Short names of parametres to retrieve
sfc_0_params = ['msl', '2t', '2d', 'tcw']  # surface, step=0
sfc_3_params = ['tp', 'cape']  # surface, step=3
sfc_6_params = ['tp', 'cape']  # surface, step=6
sfc_9_params = ['tp', 'cape']  # surface, step=9
sfc_12_params = ['tp', 'cape']  # surface, step=12
pl_params = ['u', 'v', 'w', 'r']  # model levels, step=0

# Get surface step=0 data
for param in sfc_0_params:
    for year in years:
        retrieve_era_interim(param, 'sfc', year, step='0', area=area, overwrite=False)

# Get surface step=3 data
for param in sfc_3_params:
    for year in years:
        retrieve_era_interim(param, 'sfc', year, step='3', area=area, overwrite=False)

# Get surface step=6 data
for param in sfc_6_params:
    for year in years:
        retrieve_era_interim(param, 'sfc', year, step='6', area=area, overwrite=False)

# Get surface step=9 data
for param in sfc_9_params:
    for year in years:
        retrieve_era_interim(param, 'sfc', year, step='9', area=area, overwrite=False)

# Get surface step=12 data
for param in sfc_12_params:
    for year in years:
        retrieve_era_interim(param, 'sfc', year, step='12', area=area, overwrite=False)

# Get 850hPa data
for param in pl_params:
    for year in years:
        retrieve_era_interim(param, 'pl850', year, step='0', area=area, overwrite=False)

# Get 500hPa data
for param in pl_params:
    for year in years:
        retrieve_era_interim(param, 'pl500', year, step='0', area=area, overwrite=False)
