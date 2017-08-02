"""
ecmwf_data.py:
    Download data using the ECMWF API.

Author:
    Benjamin S. Grandey, 2017
"""

from ecmwfapi import ECMWFDataServer
import os
import shutil


# Dictionary mapping parameter short names to codes
# See http://apps.ecmwf.int/codes/grib/param-db
param_dict = {
    # Surface (sfc), available at step=0 and step=3 etc
    'sp': '134',  # surface pressure
    'tcw': '136',  # total column water
    'tcwv': '137',  # total column water vapor
    'msl': '151',  # mean sea level pressure
    'tcc': '164',  # total cloud cover
    '10u': '165',  # 10 metre U wind component
    '10v': '166',  # 10 meter V wind component
    '2t': '167',  # 2 metre temperature
    '2d': '168',  # 2 metre dewpoint temperature
    'lcc': '186',  # low cloud cover
    'mcc': '187',  # medium cloud cover
    'hcc': '188',  # high cloud cover
    # Surface (sfc), available at step=3 etc but NOT step=0
    'cape': '59',  # convective available potential energy
    'tp': '228',  # total precipitation
    # Pressure levels (pl), eg 850, 500
    'z': '129',  # geopotential
    't': '130',  # temperature
    'u': '131',  # U component of wind
    'v': '132',  # V component of wind
    'q': '133',  # specific humidity
    'w': '135',  # vertical velocity
    'vo': '138',  # vorticity (relative)
    'r': '157',  # relative humidity
}


def retrieve_era_interim(param, level, year, step='0', area='Glb', nc=False, overwrite=False):
    """
    Function to retrieve ERA-Interim data from MARS via the ECMWF API.

    Args:
        param: string containing short name (e.g. '2t'; see param_dict)
        level: string containing level information (e.g. 'sfc', 'pl850')
        year: string containing year (e.g. '1979')
        step: string containing information about step (default '0')
        area: 'Glb' (global; default) or string containing bounds (N/W/S/E, e.g. '30/90/-10/120')
        nc: if True, request NetCDF format; if False (default), the files will be GRIB format
        overwrite: if True, replace existing files; if False (default), skip existing files

    Output file:
        GRIB file:
            data/ei_<area>/<param>_<code>_<level>/ei_<param>_<code>_<level>_<step>_<year>.grb
        or NetCDF file:
            data/ei_<area>/<param>_<code>_<level>_nc/ei_<param>_<code>_<level>_<step>_<year>_nc.nc
        where <code> is the parameter code (see param_dict) and <area> has '/' replaced by 'n'/'e'.

    Returns:
        0 if output file already exists
        Output filename if file is created
        -1 otherwise
    """
    print('param={}, level={}, year={}, step={}, area={}'.format(param, level, year, step, area))
    code = param_dict[param]
    area_ne = '{}n{}e{}n{}e'.format(*area.split('/'))
    if nc is True:
        out_dir = 'data/ei_{}/{}_{}_{}_nc'.format(area_ne, param, code, level)
        out_filename = 'ei_{}_{}_{}_{}_{}_nc.nc'.format(param, code, level, step, year)
    else:
        out_dir = 'data/ei_{}/{}_{}_{}'.format(area_ne, param, code, level)
        out_filename = 'ei_{}_{}_{}_{}_{}.grb'.format(param, code, level, step, year)
    # Check if output file already exists
    if os.path.exists('{}/{}'.format(out_dir, out_filename)):
        if overwrite is False:
            print('{} already exists. Skipping.'.format(out_filename))
            return 0
    # Retrieval dictionary
    retrieval_dict = {
        'class': 'ei',
        'dataset': 'interim',
        'date': '{}-01-01/to/{}-12-31'.format(year, year),
        'expver': '1',
        'grid': '0.75/0.75',
        'param': '{}.128'.format(code),
        'step': step,
        'stream': 'oper',
        'target': 'data/temp_{}'.format(out_filename),  # temporary file location
    }
    if step == '0':
        retrieval_dict['type'] = 'an'
        retrieval_dict['time'] = '00:00:00/06:00:00/12:00:00/18:00:00'
    else:
        retrieval_dict['type'] = 'fc'
        retrieval_dict['time'] = '00:00:00/12:00:00'
    if level == 'sfc':
        retrieval_dict['levtype'] = 'sfc'
    elif level[0:2] == 'pl':
        retrieval_dict['levtype'] = 'pl'
        retrieval_dict['levelist'] = level[2:]
    if area != 'Glb':
        retrieval_dict['area'] = area
    if nc is True:
        retrieval_dict['format'] = 'netcdf'
    # Retrieve data to temporary location
    server = ECMWFDataServer()
    server.retrieve(retrieval_dict)
    # If temporary file exists, move it to output file location (and create directory if necessary)
    if os.path.exists('data/temp_{}'.format(out_filename)):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            print('Created {}/'.format(out_dir))
        shutil.move('data/temp_{}'.format(out_filename), '{}/{}'.format(out_dir, out_filename))
        print('Written {}/{}'.format(out_dir, out_filename))
        result = out_dir + out_filename
    else:
        result = -1
    return result
