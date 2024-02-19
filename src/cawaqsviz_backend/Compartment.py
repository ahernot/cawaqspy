from .Config import Config
from .Mesh import Mesh
from .Observations import Observation

import json
import sys
import os
from os import sep

from .parameters import module_caw, out_caw_folder, ids_mesh, obs_types



class Compartment() : 
    
    def __init__(self, id_compartment, config, out_caw_directory, obs_directory, verbose=False) :
        super().__init__() 

        self.verbose = verbose
        if verbose: print(f'\n\nBUILDING Compartment {module_caw[id_compartment]}', flush=True)
        
        self.id_compartment = id_compartment
        self.compartment = self.defineNameCompartement(id_compartment)
        self.layers_gis_names = self.defineLayerGisName(id_compartment, config)
        self.out_caw_directory = out_caw_directory
        self.out_caw_path = self.defineOutCawPath(out_caw_directory, id_compartment)
        self.mesh = self.defineMeshCompartment(id_compartment, config)
        self.obs_path = obs_directory
        self.obs = self.defineObsCompartment(id_compartment, config)

        if verbose: print(f'{self.__repr__()}')
        if verbose: print(f'{module_caw[self.id_compartment]} has been created')      


    def __repr__(self) : 
        return f'\nCompartment {module_caw[self.id_compartment]} : \
            \n\t→ CaWaQS Outputs directory : {self.out_caw_path} \
            \n\t→ Meshes : {self.mesh}\
            \n\t→ {self.obs} \
            \n\t→ Observation path : {self.obs_path}'


    def defineNameCompartement(self, id_compartment) : 
        return module_caw[id_compartment]


    def defineLayerGisName(self, id_compartment, config) : 
        return config.resolutionNames[id_compartment][0]


    def defineOutCawPath(self, out_caw_directory, id_compartment, **kwargs):
        """
        Definie path of outputs in CaWaQS outputs directory for the define 
            compartment

        Parameters : 
            • out_caw_directory : directory contaning all CaWaQS outputs for all
                compartments
            • id_compartment : compartment ids 
        """

        # Get verbose
        verbose = kwargs.get(verbose, self.verbose)
    
        path_output_compartment = out_caw_directory + sep + \
            out_caw_folder[id_compartment] + sep

        if verbose: print(path_output_compartment)

        return path_output_compartment


    def defineMeshCompartment(self, id_compartment, config):     
        return Mesh(id_compartment, self.layers_gis_names, config, self.out_caw_directory) 


    def defineObsCompartment(self, id_compartment, config, **kwargs):

        # Get verbose
        verbose = kwargs.get(verbose, self.verbose)
        
        if id_compartment in obs_types.keys() : 
            if verbose: print(f'Building observations...')
            obs = Observation(id_compartment, id_compartment, config, self.out_caw_directory)       
            if verbose: print(f'Observations has been created')
            return obs

        else : 
            if verbose: print('Any observations for this compartment', flush=True)
            return None


    """
    def getConfig(self) :
        script_directory_with_file = os.path.abspath(__file__)
        script_directory = os.path.dirname(script_directory_with_file)  + '\\'
        sys.path.append(script_directory)

        json_config = script_directory + "Config.json"

        with open(json_config, 'r') as jsonFile :
            config = json.load(jsonFile) 
        self.config = config
    """
