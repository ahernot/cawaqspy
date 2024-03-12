"""
#/***************************************************************************
# CaWaQSViz
#
# Description
#							 -------------------
#		begin				: 2023
#		git sha				: $Format:%H$
#		copyright			: (C) 2023 by Lise-Marie GIROD
#		email				: lise-marie.girod@minesparis.psl.eu
# ***************************************************************************/
#
#/***************************************************************************
# *																		    *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	    *
# *   any later version.								    				*
# *																		    *
# ***************************************************************************/
#   BREF
#
#   CaWaQS mesh class
#
# ***************************************************************************/
"""

from .parameters import reversed_module_caw
import pandas as pd
from os import sep

from src.utils.qgis_project import QGS_PROJECT


class Mesh:
    def __init__(
        self, id_compartment, layers_gis_name: list, config, out_caw_directory
    ):
        super().__init__()

        print("Building mesh")
        self.id_compartment = id_compartment
        self.layers_gis_name = layers_gis_name
        self.config = config
        self.out_caw_directory = out_caw_directory
        self.mesh = self.GetMesh()
        self.ncells = self.getNCells()

    def __repr__(self):
        return f"{self.layers_gis_name} : {self.mesh}"

    def getNCells(self):
        ncells = 0
        for layer in self.mesh.keys():
            ncells += self.mesh[layer].ncells
        return ncells

    class Layer:
        def __init__(
            self, id_compartment, layer_gis_name: str, config, out_caw_directory
        ):
            self.id_compartment = id_compartment
            self.out_caw_directory = out_caw_directory
            self.layer = self.buildLayer(layer_gis_name, config)
            self.ncells = len(self.layer)

        def __repr__(self):
            return f"Layer count {self.ncells} cells"

        class Cell:
            def __init__(self, id_compartment, id_cell, geometry):
                self.id = id_cell  # id int of the cells
                self.geometry = geometry  # geometry of the cells
                self.area = geometry.area()  # in meters

            def __repr__(self):
                return f"id : {self.id} ({round(self.area, 1) * 1e-4} ha)"

        def buildLayer(self, layer_gis_name, config):
            gis_layer = QGS_PROJECT.mapLayersByName(layer_gis_name)[0]
            n_col = int(config.idColCells[self.id_compartment])

            layer = []
            print("Bulding layer ...", flush=True)

            if self.id_compartment != reversed_module_caw["HYD"]:
                for entitie in gis_layer.getFeatures():
                    id_cell = entitie.attributes()[n_col]

                    if id_cell >= 0:
                        geometry_cell = entitie.geometry()

                        layer.append(
                            self.Cell(self.id_compartment, id_cell, geometry_cell)
                        )

                    else:
                        pass

            else:
                corr_file = self.readHydCorrespfile(self.out_caw_directory)
                for entitie in gis_layer.getFeatures():
                    id_gis = entitie.attributes()[n_col]
                    id_int = corr_file["ID_ABS"].loc[id_gis]
                    geometry_cell = entitie.geometry()

                    layer.append(self.Cell(self.id_compartment, id_int, geometry_cell))

            return layer

        def readHydCorrespfile(self, out_caw_directory):
            print(f"reading hyd corresp file : {out_caw_directory}")
            corresp_file_path = out_caw_directory + sep + "HYD_corresp_file.txt"

            corr = pd.read_csv(corresp_file_path, index_col=2, sep="\s+")

            return corr

    def GetMesh(self):
        """
        Get Mesh from gis layers
        """
        layers = {}

        for id_layer, layer_gis_name in enumerate(self.layers_gis_name):
            layers[id_layer] = self.Layer(
                self.id_compartment, layer_gis_name, self.config, self.out_caw_directory
            )
        return layers
