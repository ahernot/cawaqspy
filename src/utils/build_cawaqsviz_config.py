import os
import json


DIRPATH_DATA = '/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE'
DIRPATH_OBS  = '/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/DATA_OBS/TS_OBS_DISCHARGE'
DIRPATH_OUT  = '/home/anatole/Documents/DATA_CAWAQS_OUT/'  # os.makedirs
dirname_out_proj = 'Project'
dirpath_out_proj = '/home/anatole/Documents/DATA_CAWAQS_OUT/Project'  # TODO: iterate over project_{id}
DIRPATH_POST_PROCESSING = '/home/anatole/Documents/DATA_CAWAQS_OUT/Project/POST_PROCESSING'  # TODO: main PP dir (includes all PP subdirs)

path_config_project = os.path.join(dirpath_out_proj, f'config_project_{dirname_out_proj}.json')
path_config_geometries = os.path.join(dirpath_out_proj, f'config_geometries_{dirname_out_proj}.json')



config_geometries_dict = {
    'ids_compartment': [3, 2],
    'resolutionNames': {
        '3': [['ELEMENTS_BU']],
        '2': [['ELEMENTS_MUSKINGUM']]
    },
    'ids_col_cell': {
        '3': 2,
        '2': 13
    },
    'obsNames':        {'2': 'STATIONS_select'},
    'obsIdsColCells':  {'2': 5},
    'obsIdsColNames':  {'2': 0},
    'obsIdsColLayers': {'2': None}
}

config_project_dict = {
    'json_path_geometries': os.path.join(dirpath_out_proj, f'config_geometries_{dirname_out_proj}.json'),
    'projectName':          dirname_out_proj,
    'cawOutDirectory':      os.path.join(dirpath_out_proj, f'RUN_CAL_1'),
    'startSim':             2005,
    'endSim':               2023,
    'obsDirectory':         DIRPATH_OBS,
    'ppDirectory':          DIRPATH_POST_PROCESSING
}

def build ():
    # Build geometries config file
    with open(path_config_geometries, 'w', encoding='utf-8') as file:
        json.dump(config_geometries_dict, file, indent=4)
    
    # Build project config file
    with open(path_config_project, 'w', encoding='utf-8') as file:
        json.dump(config_project_dict, file, indent=4)
