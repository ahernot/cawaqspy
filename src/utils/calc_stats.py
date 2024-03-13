import os
import subprocess
import json
import pandas as pd

from src.cawaqsviz_backend.Config import ConfigGeometry
from src.cawaqsviz_backend.ExploreData import ExploreData
from src.cawaqsviz_backend.StatisticalCriteria import StatisticalCriteria

from src.resources.json_encoders import NumpyEncoder
from src.utils.build_command_file import build_command_file
from src.utils.build_cawaqsviz_config import build_config_geometries, build_config_project
from src.config import *



# Run with a DONSUR path
def calc_stats (proj_name: str, obstype: str, **kwargs) -> dict:  # TODO: DONSUR path <= wrap calc_pbiases in an iterative scanning function generating dirname_proj and donsur on the fly
    """
    Simulate and calculate stats for a given project and observation type using CaWaQS + CaWaQSViz.

    Args:
        proj_name (str): Name of the project (no spaces, no special characters)
        obstype (str): Observation type ('Discharge', 'Hydraulic Head')

    Kwargs:
        save (bool): Save pbiases as json and csv (default: True)
        verbose (bool): Print debug information (default: False)
        run_cawaqs (bool): Run CaWaQS (default: True)
        run_cawaqsviz (bool): Run CaWaQSViz post-processing (default: True)

    Returns:
        dict: Dictionary of statistical criteria
    """

    # Read kwargs
    verbose = kwargs.get('verbose', False)


    # Build main project directory
    dirname_proj = proj_name
    dirpath_proj = os.path.join(DIRPATH_OUT, dirname_proj)
    try:
        os.makedirs(dirpath_proj)
    except FileExistsError:
        pass

    
    # CaWaQS
    run_cawaqs = kwargs.get('run_cawaqs', True)
    if run_cawaqs:

        # Build CaWaQS command file
        DIRPATH_COMM = os.path.join(DIRPATH_DATA, 'Cmd_files')
        path_command_file = os.path.join(DIRPATH_COMM, f'{dirname_proj}.COMM')
        build_command_file(  # TODO: deprecate
            path_command_file,
            include_hydro_aquifer = True,
            dirpath_data = DIRPATH_DATA,
            dirpath_output = dirpath_proj,
            n_threads = 8,
            donsur = 'DONSUR_BU28.txt',
            lien_bu_mto = 'LIEN_BU28_MTO.txt',
            verbose = verbose
        )

        # Run CaWaQS from command line
        path_log = os.path.join(dirpath_proj, f'{dirname_proj}.log')
        command = f'{PATH_CAWAQS} "{path_command_file}" "{path_log}"'
        if verbose: print(command)
        # Run command
        if verbose: os.system(command)
        else: subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)  # TODO: catch errors

        # TODO: Remove mac5_2_0_* file



    # CaWaQSViz
    run_cawaqsviz = kwargs.get('run_cawaqsviz', True)
    if run_cawaqsviz:
        
        # Build CaWaQSViz post-processing directory inside of the project directory
        dirpath_proj_postproc = os.path.join(dirpath_proj, DIRNAME_PROJ_POSTPROC)
        try:
            os.makedirs(dirpath_proj_postproc)
        except FileExistsError:
            pass

        # Build CaWaQSViz temp directory
        dirpath_proj_postproc_temp = os.path.join(dirpath_proj_postproc, 'TEMP')
        os.makedirs(dirpath_proj_postproc_temp, exist_ok=True)  # Overwrite if needed  

        # Build CaWaQSViz geometries config file
        config_geometries_dict, path_config_geometries = build_config_geometries(
            save = True,
            dirpath_proj = dirpath_proj,
            verbose = verbose
        )
        config_geometry = ConfigGeometry.fromUnformattedDict(config_geometries_dict)

        # Build CaWaQSViz project config file
        config_project_dict, path_config_project = build_config_project(
            dirpath_proj = dirpath_proj,
            path_config_geometries = path_config_geometries,
            year_start = 2005,
            year_stop = 2023,
            dirpath_obs = DIRPATH_OBS,
            dirpath_proj_postproc = dirpath_proj_postproc,
            save = True,
            verbose = verbose
        )

        # Generate CaWaQSViz ExploreData instance    
        exd = ExploreData(
            ids_compartments = config_geometry.idCompartments,
            config = config_geometry,
            out_caw_directory = os.path.join(dirpath_proj, DIRNAME_PROJ_ITER),
            obs_directory = DIRPATH_OBS,
            post_process_directory = dirpath_proj_postproc,
            s_year = YEAR_START + 1,  # TODO: start in YEAR_START+1
            e_year = YEAR_STOP,
            dirpath_temp = dirpath_proj_postproc_temp
        )

        # Compute pbiases using CaWaQSViz
        sc = StatisticalCriteria(exd=exd, obstype=obstype, unit='l/s')
        stats_dict = sc.run()

        # Save pbiases
        save = kwargs.get('save', True)
        if save:
            # Save pbiases as json
            path_out_json = os.path.join(dirpath_proj_postproc, 'stats.json')
            with open(path_out_json, 'w', encoding='utf-8') as f:
                json.dump(stats_dict, f, ensure_ascii=False, indent=4, cls=NumpyEncoder)

            # Save pbiases as csv
            path_out_csv = os.path.join(dirpath_proj_postproc, 'stats.csv')
            df = pd.DataFrame(stats_dict)
            df.to_csv(path_out_csv, index=True, index_label='metric', header=True, sep=',')

            if verbose:
                print(f'Saved outputs in {dirpath_proj_postproc}')

        return stats_dict
    return None  # No statistics computed
