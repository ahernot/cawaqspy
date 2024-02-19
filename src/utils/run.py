import os

from src.utils import build_command_file
from src.config import *



# Run with a DONSUR path
def run (verbose = False):

    # Build output directory
    dirname_out_proj = 'TestProj'
    dirpath_out_proj = os.path.join(DIRPATH_OUT, dirname_out_proj)

    try:
        os.makedirs(dirpath_out_proj)
    except FileExistsError:
        pass
    

    build_command_file.DIRPATH_DATA = DIRPATH_DATA
    build_command_file.DIRPATH_OUTPUT = dirpath_out_proj
    build_command_file.N_THREADS = 8
    build_command_file.DONSUR = 'DONSUR_BU28.txt'  # TODO: generate on the fly
    build_command_file.LIEN_BU_MTO = 'LIEN_BU28_MTO.txt'
    build_command_file.LIEN_ELE_BU_CPROD = 'LIEN_ELE_BU_CPROD.txt'

    # Build command file
    DIRPATH_COMM = os.path.join(DIRPATH_DATA, 'Cmd_files')
    path_command_file = os.path.join(DIRPATH_COMM, f'{dirname_out_proj}.COMM')
    build_command_file.build(path_command_file)
    if verbose: print(f'Built command file in path "{path_command_file}"')