from .Compartment import Compartment
from .Manage import Manage
# from PyQt5.QtCore import QObject, pyqtSignal

from os import sep



class ExploreData() : 

    _explore_data_instance = None

    def __init__(self, ids_compartments, config, out_caw_directory, obs_directory, post_process_directory, s_year, e_year, dirpath_temp: str):
        self.manage = Manage()
        self.ids_compartments = ids_compartments
        self.config = config
        self.compartments = self.definiCompartments(ids_compartments, config, out_caw_directory, obs_directory)
        self.post_process_directory = post_process_directory
        self.temp_directory = dirpath_temp  # post_process_directory + sep + 'TEMP'
        # self.temporyfilemanager = TemporyFileManager()
        self.startsim = s_year
        self.endsim = e_year
    
      
    def __repr__(self): 
        return f"EXPLORE DATA : \nSTART SIM : {self.startsim}\n END SIM : {self.endsim}\n ID Compartment : {self.ids_compartments}, \n CONFIG : {self.config}, \n"

    @classmethod
    def set_instance(cls, explore_data_instance, verbose=False):
        cls._explore_data_instance = explore_data_instance
        if verbose: print(explore_data_instance)

    @classmethod
    def get_instance(cls):
        return cls._explore_data_instance

    def definiCompartments(self, ids_compartments, config, out_caw_directory, obs_directory) :
        compartments = {}

        for id_c in ids_compartments : 
            compartments[id_c] = Compartment(id_c, config, out_caw_directory, obs_directory)

        return compartments
