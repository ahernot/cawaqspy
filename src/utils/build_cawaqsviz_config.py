import os
import json

from src.config import *



DIRPATH_PROJ = '/home/anatole/Documents/DATA_CAWAQS_OUT/Project'  # TODO: iterate over project_{id}
DIRPATH_PROJ_POSTPROC = '/home/anatole/Documents/DATA_CAWAQS_OUT/Project/POST_PROCESSING'  # TODO: main PP dir (includes all PP subdirs)
YEAR_START = 2005
YEAR_STOP = 2023

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



def build_config_geometries (**kwargs) -> dict:  # TODO: option to 
    """_summary_

    Kwargs:
        save (bool): Save as a JSON file
        path (str): Save path
        verbose (bool):

        dirpath_out_proj (str): For saving the file only

    Returns:
        dict: _description_
    """
    
    save = kwargs.get('save', False)
    verbose = kwargs.get('verbose', False)

    # Save config to JSON
    if save:
        dirpath_out_proj = kwargs.get('dirpath_out_proj', DIRPATH_PROJ)
        dirname_out_proj = os.path.split(DIRPATH_PROJ)[-1]
        path_config_geometries = kwargs.get('path', os.path.join(dirpath_out_proj, f'config_geometries_{dirname_out_proj.lower()}.json'))
        
        with open(path_config_geometries, 'w', encoding='utf-8') as file:
            json.dump(config_geometries_dict, file, indent=4)
        if verbose: print(f'Saved geometries config file in "{path_config_geometries}"')

    return config_geometries_dict


def build_config_project (**kwargs) -> dict:
    """_summary_

    Kwargs:
        save (bool): Save as a JSON file
        path (str): Save path
        verbose (bool)

        dirpath_out_proj (str):
        path_config_geometries (str):
        year_start (int)
        year_stop (int)
        dirpath_obs (str)
        dirpath_proj_postproc (str)  # TODO dirpath_post_processing

    Returns:
        dict: _description_
    """

    dirpath_out_proj = kwargs.get('dirpath_out_proj', DIRPATH_PROJ)
    dirname_out_proj = os.path.split(DIRPATH_PROJ)[-1]
    
    # Build config dict
    config_project_dict = {
        'json_path_geometries': kwargs.get('path_config_geometries', os.path.join(dirpath_out_proj, f'config_geometries_{dirname_out_proj.lower()}.json')),
        'projectName':          dirname_out_proj,
        'cawOutDirectory':      os.path.join(dirpath_out_proj, DIRNAME_PROJ_ITER),
        'startSim':             kwargs.get('year_start', YEAR_START),
        'endSim':               kwargs.get('year_stop', YEAR_STOP),
        'obsDirectory':         kwargs.get('dirpath_obs', DIRPATH_OBS),
        'ppDirectory':          kwargs.get('dirpath_proj_postproc', DIRPATH_PROJ_POSTPROC)
    }

    # Save config to JSON
    save = kwargs.get('save', False)
    verbose = kwargs.get('verbose', False)
    if save:
        path_config_project = kwargs.get('path', os.path.join(dirpath_out_proj, f'config_project_{dirname_out_proj}.json'))  # TODO
        with open(path_config_project, 'w', encoding='utf-8') as file:
            json.dump(config_project_dict, file, indent=4)
        if verbose: print(f'Saved project config file in "{path_config_project}"')

    return config_project_dict
