import os
import json
from typing import Union

from src.config import *

# Default values
DIRPATH_PROJ = os.path.join(DIRPATH_OUT, DIRNAME_PROJ)  # TODO: iterate over project_{id}
DIRPATH_PROJ_POSTPROC = os.path.join(DIRPATH_PROJ, DIRNAME_PROJ_POSTPROC)


# config_geometries_dict = {
#     'ids_compartment': [3, 2],
#     'resolutionNames': {
#         '3': [['ELEMENTS_BU']],
#         '2': [['ELEMENTS_MUSKINGUM']]
#     },
#     'ids_col_cell': {
#         '3': 2,
#         '2': 13
#     },
#     'obsNames':        {'2': 'STATIONS_select'},
#     'obsIdsColCells':  {'2': 5},
#     'obsIdsColNames':  {'2': 0},
#     'obsIdsColLayers': {'2': None}
# }

config_geometries_dict = {
    'ids_compartment': [1, 2, 3, 4],
    'resolutionNames': {
        '1': [['AQ_GRID_TERT'], ['AQ_GRID_CRAI'], ['AQ_GRID_JURA']],
        '2': [['ELEMENTS_MUSKINGUM']],
        '3': [['ELEMENTS_BU']],
        '4': [['PARAM_NSAT']]
    },
    'ids_col_cell': {
        '1': 5,
        '2': 13,
        '3': 2,
        '4': 0
    },
    'obsNames': {'2': 'STATIONS_select','1': 'Piezo_select'},
    'obsIdsColCells': {'2': 5, '1': 0},
    'obsIdsColNames': {'2': 0, '1': 4},
    'obsIdsColLayers': {'2': None, '1': 15}
}



def build_config_geometries (**kwargs) -> Union[dict, str]:  # TODO: option to 
    """_summary_

    Kwargs:
        save (bool): Save as a JSON file
        path (str): Save path
        verbose (bool):

        dirpath_proj (str): For saving the file only

    Returns:
        dict: _description_
    """
    
    save = kwargs.get('save', False)
    verbose = kwargs.get('verbose', False)

    # Save config to JSON
    if save:
        dirpath_proj = kwargs.get('dirpath_proj', DIRPATH_PROJ)
        dirname_proj = os.path.split(DIRPATH_PROJ)[-1]
        path_config_geometries = kwargs.get('path', os.path.join(dirpath_proj, f'config_geometries_{dirname_proj.lower()}.json'))
        
        with open(path_config_geometries, 'w', encoding='utf-8') as file:
            json.dump(config_geometries_dict, file, indent=4)
        if verbose: print(f'Saved geometries config file in "{path_config_geometries}"')

        return config_geometries_dict, path_config_geometries

    return config_geometries_dict, ''


def build_config_project (**kwargs) -> Union[dict, str]:
    """_summary_

    Kwargs:
        save (bool): Save as a JSON file
        path (str): Save path
        verbose (bool)

        dirpath_proj (str):
        path_config_geometries (str):
        year_start (int)
        year_stop (int)
        dirpath_obs (str)
        dirpath_proj_postproc (str)

    Returns:
        dict, str: _description_
    """

    dirpath_proj = kwargs.get('dirpath_proj', DIRPATH_PROJ)
    dirname_proj = os.path.split(DIRPATH_PROJ)[-1]
    
    # Build config dict
    config_project_dict = {
        'json_path_geometries': kwargs.get('path_config_geometries', os.path.join(dirpath_proj, f'config_geometries_{dirname_proj.lower()}.json')),
        'projectName':          dirname_proj,
        'cawOutDirectory':      os.path.join(dirpath_proj, DIRNAME_PROJ_ITER),
        'startSim':             kwargs.get('year_start', YEAR_START),
        'endSim':               kwargs.get('year_stop', YEAR_STOP),
        'obsDirectory':         kwargs.get('dirpath_obs', DIRPATH_OBS),
        'ppDirectory':          kwargs.get('dirpath_proj_postproc', DIRPATH_PROJ_POSTPROC)
    }

    # Save config to JSON
    save = kwargs.get('save', False)
    verbose = kwargs.get('verbose', False)
    if save:
        path_config_project = kwargs.get('path', os.path.join(dirpath_proj, f'config_project_{dirname_proj.lower()}.json'))
        with open(path_config_project, 'w', encoding='utf-8') as file:
            json.dump(config_project_dict, file, indent=4)
        if verbose: print(f'Saved project config file in "{path_config_project}"')
        return config_project_dict, path_config_project

    return config_project_dict, ''
