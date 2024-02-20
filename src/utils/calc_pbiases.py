import os
import subprocess

# from src.cawaqsviz_backend.Config import ConfigGeometry
# from src.cawaqsviz_backend.ExploreData import ExploreData
# from src.cawaqsviz_backend.StatisticalCriteria import StatisticalCriteria

from src.utils.build_command_file import build_command_file
from src.utils.build_cawaqsviz_config import build_config_geometries
from src.config import *



# Run with a DONSUR path
def calc_pbiases (**kwargs) -> dict:  # TODO: DONSUR path <= wrap calc_pbiases in an iterative scanning function generating dirname_proj and donsur on the fly
    """_summary_

    Kwargs:
        dirname_proj (str):
        dirname_proj_postproc (str):
        verbose (bool): 

    Returns:
        dict: _description_
    """

    # Read kwargs
    verbose = kwargs.get('verbose', False)



    # Build main project directory
    dirname_proj = kwargs.get('dirname_proj', DIRNAME_PROJ)
    dirpath_proj = os.path.join(DIRPATH_OUT, dirname_proj)
    try:
        os.makedirs(dirpath_proj)
    except FileExistsError:
        pass

    # Build CaWaQS command file
    DIRPATH_COMM = os.path.join(DIRPATH_DATA, 'Cmd_files')
    path_command_file = os.path.join(DIRPATH_COMM, f'{dirname_proj}.COMM')
    build_command_file(
        path_command_file,
        dirpath_data = DIRPATH_DATA,
        dirpath_output = dirpath_proj,
        n_threads = 8,
        donsur = 'DONSUR_BU28.txt',
        lien_bu_mto = 'LIEN_BU28_MTO.txt',
        verbose = verbose
    )

    # Run CaWaQS from command line
    path_log = os.path.join(dirpath_proj, f'{dirname_proj}.log')
    command = f'{PATH_CAWAQS} {path_command_file} {path_log}'
    if verbose: print(command)
    # os.system(command)  # TODO: --quiet
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)



    # Build CaWaQSViz post-processing directory inside of the project directory
    dirname_proj_postproc = kwargs.get('dirname_proj_postproc', DIRNAME_PROJ_POSTPROC)
    dirpath_proj_postproc = os.path.join(dirpath_proj, dirname_proj_postproc)
    try:
        os.makedirs(dirpath_proj_postproc)
    except FileExistsError:
        pass

    # # Build CaWaQSViz geometries config file
    # config_geometries_dict = build_config_geometries()
    # config_geometry = ConfigGeometry.fromUnformattedDict(config_geometries_dict)

    # # Generate CaWaQSViz ExploreData instance    
    # exd = ExploreData(
    #     ids_compartments=config_geometry.idCompartments,
    #     config=config_geometry,
    #     out_caw_directory=os.path.join(dirpath_proj, DIRNAME_PROJ_ITER),
    #     obs_directory=DIRPATH_OBS,
    #     post_process_directory=dirpath_proj_postproc,
    #     s_year=YEAR_START+1,  # TODO: start in YEAR_START+1
    #     e_year=YEAR_STOP
    # )

    # # Compute pbiases using CaWaQSViz
    # sc = StatisticalCriteria(exd=exd)
    # pbiases_dict = sc.run()

    # return pbiases_dict
