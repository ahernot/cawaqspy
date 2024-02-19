from .parameters import obs_types, out_caw_folder, link_obs_mesh, reversed_module_caw

from os import sep
import pandas as pd

from qgis.core import QgsProject, QgsSpatialIndex, QgsPointXY



class Observation() :
    def __init__(self, id_obs, id_compartment, config, out_caw_directory):
        
        
        self.id_compartment = id_compartment
        self.id_obs     = id_obs
        self.config     = config
        self.obs_type   = self.defineObsType(id_obs)
        self.id_mesh       = self.defineIdMesh(id_obs)
        self.out_caw_directory = out_caw_directory
        

        self.layer_gis_name = self.defineLayerGisName(id_obs)
        self.out_caw_path   = self.defineOutCawPath(id_obs)
        # self.id_mesh        = self.defineIdMesh(id_obs)
        self.obs_points     = self.defineObsPoints(id_obs, self.layer_gis_name)
        self.n_obs          = len(self.obs_points)
        
               
    def __repr__(self):
        return f'Observations : {self.n_obs} {self.obs_type}(s)'

    def defineObsType(self, id_obs) : 
        return obs_types[id_obs]

    def defineLayerGisName(self, id_obs) :
        return self.config.obsNames[id_obs]

    def defineOutCawPath(self, id_obs):
        return out_caw_folder[id_obs]
    
    def defineIdMesh(self, id_obs):
        return link_obs_mesh[id_obs]

    def readHydCorrespfile(self, out_caw_directory, verbose=False) :
        if verbose: print(f'reading hyd corresp file : {out_caw_directory}') 
        corresp_file_path = out_caw_directory + sep + 'HYD_corresp_file.txt'
        
        corr = pd.read_csv(corresp_file_path, index_col = 2, sep = '\s+')

        return corr

    def getCloserCell(self, obs_geom, id_layer, verbose=False) :   
        """
        Returns the cell closest to the measurement point 

        Parameters : 
            obs_geom : geometry of the observation point 
            id_mesh : mesh id
            id_layer : layer id
        """   
        """ if verbose: print(self.id_compartment, id_layer)
        if verbose: print(self.config.resolutionNames[self.id_compartment][0][id_layer]) """
        gis_layer   = QgsProject.instance().mapLayersByName(\
            self.config.resolutionNames[self.id_compartment][id_layer][0])[0]

        # if verbose: print(f'GIS layer used to get closer cell : {gis_layer}')
    
        spatial_idx = QgsSpatialIndex(gis_layer.getFeatures())
        spatial_idx_nearestCell = spatial_idx.nearestNeighbor(obs_geom, 1)[0]
        nearestCell = gis_layer.getFeature(spatial_idx_nearestCell)
        id_cell     = nearestCell.attributes()[int(self.config.idColCells[self.id_compartment])] if nearestCell else None

        if self.id_compartment == reversed_module_caw['HYD'] : 
            corr = self.readHydCorrespfile(self.out_caw_directory)
            id_cell = corr['ID_ABS'].loc[id_cell]


        return id_cell

    def defineObsPoints(self, id_obs, layer_gis_name):
        id_obs      = int(id_obs)
        config      = self.config
        obs_points  = []
        gis_layer   = QgsProject.instance().mapLayersByName(layer_gis_name)[0]
        obs_points  = []

        for entitie in gis_layer.getFeatures() :
            id_point    = entitie.attributes()[int(config.obsIdsColCells[id_obs])]
            name_point  = entitie.attributes()[int(config.obsIdsColNames[id_obs])]

            if config.obsIdsColLayer[id_obs] != None :
                id_layer = entitie.attributes()[int(config.obsIdsColLayer[id_obs])]
            else : 
                id_layer = 0
            
                    
            geometry_point = entitie.geometry()

            # Define closer cell in layer in mesh
            id_cell = self.getCloserCell(geometry_point, id_layer)

            
            obs_points.append(self.ObsPoint(id_point, geometry_point, name_point, id_layer, id_cell, self.id_mesh))

        # if verbose: print(len(obs_points))
        return obs_points

    class ObsPoint() : 
        def __init__(self, id_point, geometry_point, name, id_layer, id_cell, id_mesh, verbose=False) : 
            self.id_gis = id_point
            self.geometry = geometry_point
            self.name = name
            self.id_mesh = id_mesh
            self.id_layer = id_layer
            self.id_cell = id_cell
            self.obstimeserie = None
            self.simtimeserie = None
            if verbose: print(self.__repr__())

        def __repr__(self) : 
            return f'{self.id_gis} : {self.name} (linked to cell {self.id_cell} of layer {self.id_layer} of mesh {self.id_mesh})'
            # if verbose: print(self.id_gis)
