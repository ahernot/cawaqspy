import json
from .Factory import FactoryClass

from .parameters import module_caw, ids_mesh, reversed_module_caw

class Config(FactoryClass):
    def __init__(self, a_dict):
        self.a_dict = a_dict
                
    def writeJsonConfig(self, jsonPath) :
        with open(jsonPath, 'w') as json_file : 
            json.dump(self.a_dict, json_file)

    def extractAllResolutionName(self) : 
        mesh_to_RN = {}    

        for key in self.idCompartments : 
            
            compartmentRN =  self.exctractItemsInList(self.resolutionNames[key])
            compartmentIdMesh   = ids_mesh[key]

            if len(compartmentRN) == len(compartmentIdMesh) :
                for RN, idmesh in zip(compartmentRN, compartmentIdMesh) : 
                    mesh_to_RN[idmesh] = RN
         
            elif len(compartmentIdMesh) == 1 : 
                mesh_to_RN[compartmentIdMesh[0]] = compartmentIdMesh

            else : 
                pass

        if mesh_to_RN : 
            return mesh_to_RN

    def exctractItemsInList(self, lists) : 
        items = []

        for item in lists:
            if isinstance(item, list):
                items.extend(self.exctractItemsInList(item))
            else:
                items.append(item)

        return items

    def reverseDict(self, dict_to_reverse) : 
        return {value : key for key, value in dict_to_reverse.items()}

    def exctractCompartmentFromResolutionNames(self, resolutionName) :
        for key, values in self.resolutionNames.items() :
            if any(resolutionName in sub_list for sub_list in values) : 
                return key
            else : 
                return None

class ConfigGeometry(Config) : 
    def __init__(self, a_dict) :
        super(ConfigGeometry, self).__init__(a_dict)

        self.idCompartments     = a_dict['ids_compartment']
        self.resolutionNames    = a_dict["resolutionNames"]
        self.idColCells         = a_dict['ids_col_cell']

        # obs configuration 
        self.obsNames       = a_dict["obsNames"]
        self.obsIdsColCells = a_dict["obsIdsColCells"]
        self.obsIdsColNames = a_dict["obsIdsColNames"]
        self.obsIdsColLayer = a_dict["obsIdsColLayers"]


    def __repr__(self) : 
        return f'\nGEOMETRIES CONFIG : \n\
            Compartments : {[module_caw[id_c] for id_c in self.idCompartments]}\n\
            MESH CONFIG : \n\
                \tLayers gis names : {[res for res in self.resolutionNames.values()]}\n\
                \tId of col in dfb containing cells ids : {self.idColCells}\n\
            OBS CONFIG :\n\
                \tLayer gis names : {self.obsNames}\n\
                \tId of col in dfb containing mps ids : {self.obsIdsColCells}\n\
                \tId of col in dfb containing mps names : {self.obsIdsColNames}\n\
                \tId of col in dfb containing mps aq layer : {self.obsIdsColLayer}\n\
                '

class ConfigProject(Config) : 
    def __init__(self, a_dict) :
        super(ConfigProject, self).__init__(a_dict)
        self.json_path_geometries   = a_dict['json_path_geometries']
        self.projectName            = a_dict['projectName']
        self.cawOutDirectory        = a_dict['cawOutDirectory']
        self.startSim               = a_dict['startSim']
        self.endsim                 = a_dict['endSim']
        self.obsDirectory           = a_dict['obsDirectory']
        self.ppDirectory            = a_dict['ppDirectory']

    def __repr__(self) : 
        return f"\
                \nPROJECT CONFIG : \n\
                \nProject Name : {self.projectName}\
                \nDirectory of CaWaQS output : {self.cawOutDirectory}\
                \nDirectory of Observation data : {self.obsDirectory}\
                \nPost-Process directory : {self.ppDirectory}\
                "


