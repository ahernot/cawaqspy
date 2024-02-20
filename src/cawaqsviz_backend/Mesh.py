# from .Compartment import Compartment
# from .Cell import Cell

# from qgis.core import QgsProject, QgsVectorLayer, QgsGeometry

from .parameters import names_mesh, ids_mesh, reversed_module_caw 
import pandas as pd
from os import sep

from src.utils.qgis_project import QGS_PROJECT


# Define QGIS instance from QGS file
# QGS_PROJECT = QgsProject.instance()
# QGS_PROJECT.read('/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/Projet_SIG/Modele_Seine_Simple_DataSelected2024.qgs')




class Mesh() :
    def __init__(self, id_compartment, layers_gis_name : list, config, out_caw_directory, verbose=False):
        super().__init__()

        # self.ncells = None
        if verbose: print(f'Building mesh')
        self.id_compartment = id_compartment
        self.layers_gis_name = layers_gis_name
        self.config = config
        self.out_caw_directory = out_caw_directory
        self.mesh= self.GetMesh()

    def __repr__(self) : 
        return f'{self.layers_gis_name} : {self.mesh}'
        
    class Layer() : 

        def __init__(self, id_compartment, layer_gis_name : str, config, out_caw_directory):
            self.id_compartment = id_compartment
            self.out_caw_directory = out_caw_directory
            self.layer = self.buildLayer(layer_gis_name, config)
            self.ncells = len(self.layer)
            
        
        def __repr__(self) : 
            return f'Layer count {self.ncells} cells' 

        class Cell() : 
            def __init__(self, id_compartment, id_cell, geometry) : 
                self.id = id_cell           # id int of the cells
                self.geometry = geometry    # geometry of the cells
                self.area = geometry.area() # in meters

            def __repr__(self) : 
                return f'id : {self.id} ({round(self.area, 1) * 1e-4} ha)'
        
        def buildLayer(self, layer_gis_name, config, verbose=False):
            # print(QGS_PROJECT.mapLayers())
            gis_layer = QGS_PROJECT.mapLayersByName(layer_gis_name)[0]
            n_col = int(config.idColCells[self.id_compartment])

            layer = []
            if verbose: print('Bulding layer ...', flush=True)

            if self.id_compartment != reversed_module_caw['HYD']:

                for entitie in gis_layer.getFeatures() :
                    
                    id_cell = entitie.attributes()[n_col]

                    if id_cell >= 0 :            
                        geometry_cell = entitie.geometry()
                        
                        layer.append(self.Cell(self.id_compartment, id_cell, geometry_cell))

                    else :
                        pass

            else : 
                corr_file = self.readHydCorrespfile(self.out_caw_directory)
                for entitie in gis_layer.getFeatures():
                    id_gis = entitie.attributes()[n_col]
                    id_int = corr_file['ID_ABS'].loc[id_gis]
                    geometry_cell = entitie.geometry()

                    layer.append(self.Cell(self.id_compartment, id_int, geometry_cell))

            return layer

        def readHydCorrespfile(self, out_caw_directory, verbose=False) :
            if verbose: print(f'reading hyd corresp file : {out_caw_directory}') 
            corresp_file_path = out_caw_directory + sep + 'HYD_corresp_file.txt'
            
            corr = pd.read_csv(corresp_file_path, index_col = 2, sep = '\s+')

            return corr

    def GetMesh(self):
        """
        Get Mesh from gis layers            
        """
        layers = {}

        for id_layer, layer_gis_name in enumerate(self.layers_gis_name) :
            layers[id_layer] = self.Layer(self.id_compartment, layer_gis_name, self.config, self.out_caw_directory)
        return layers

    