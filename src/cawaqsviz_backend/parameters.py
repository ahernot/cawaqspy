## DEFAULT REPOSITORY
default_rep = {
    "CONFIG" : "",
    "OBS" : "/home/cawaqs-by-mines/DATA_CAWAQS/SEINE_3C/DATA_OBS/TS_OBS_DISCHARGE",
    "PP"  : 'U:/CAWAQS/testcases/datasets/coupled_hydro/pp_coupled', 
    "OUT_CAW" : 'U:/CAWAQS/OUTPUTS_CAWAQS/OUTPUTS_LOING/FP_PARAM_DONSUR_SEINE',
}

# CAWAQS COMPARTMENTS
# cawaqs module
module_caw = {
    1 : "AQ", 
    2 : "HYD", 
    3 : "WATBAL", 
    4 : "NSAT",
}

reversed_module_caw = inversed_module_caw = {
    value: key for key, value in module_caw.items()
    }

# output folder in cawaqs output directory
out_caw_folder = {
    1 : "Output_AQ", 
    2 : "Output_HYD", 
    3 : "Output_WATBAL", 
    4 : "Output_NSAT",
}

# Meshes ids 
ids_mesh = {
    1 : [1], 
    2 : [2], 
    3 : [3], 
    4 : [4], 
}

mesh_to_compartment = {
    1 : 1,
    2 : 2,
    3 : 3,
    4 : 4, 

}

# SHAPEFILES/DATABASEFILE CONFIG OF COMPARTMENTS 
## Meshes layers names in gis project
names_mesh = {
    1 : 'Aq',
    2 : 'Elemusk',
    3 : 'Sectmusk',
    4 : 'Cprod',
    5 : 'Elebu', 
    6 : 'Nsat'
}

## /!\ lists imbrication matter !
## 2nd order is mesh, 3rd order is for layer 
## exemple : Aquifere compartment count 1 mesh but many layers
##           Watbal compartement count 4 meshes but 1 layer per mesh
layers_GIS_names = {
    1 : [["ALLU", "DSOL", "PITH", "ETAM", "CBSF", "CCCL", "TERT", "CRAI", 'JURA']],
    2 : [["ELEMENTS_MUSKINGUM"], ["NETWORK_MUSKINGUM"]],
    3 : [["CPROD"], ["ELEBU"]], 
    4 : [["NSAT"]]
}


## number of the column in the attribute 
## table containing the cell's internal id
col_id_int = {
    1 : 2 , # 'Aq'
    2 : 6 , # 'Elements'
    3 : 1, # 'SectMusk'
    4 : 0 , # 'Cprod'
    5 : 0 , # 'Elebu' 
    6 : 0 , # 'Nsat'
}

# OBSERVATIONS (key : id_compartment, value = obs type)
## observation type
obs_types = {
    1 : 'Piezometer',
    2 : 'Station',     
}

## Observation layers in gis project
obs_gis_name = {
    1 : 'PIEZOMETERS',
    2 : 'STATIONS',
}

## Link observation object to compartment (key = id_obs (id_compartment), 
## value = id_compartement)
link_obs_mesh = {   
    1 : 1, # piezometer → Aq 
    2 : 3, # station → Elemusk
}

## id of column in DBF countaining the id of observation point
obs_col_id = {
    1 : 1, # piezometers
    2 : 2, # station
    
}

## id of column in DBF countaining the name of observation point
obs_col_name = {
    1 : 6, # piezometer
    2 : 0, # station
    
}

## id of column in DBF countaining the mesh layer 
## of observation point
obs_col_layer = {
    1 : 26, # piezometer
    2 : 46, # station
    
    
}

# BINARY FILES CONFIG
binfiles_type = {
    1 : 'AQ' , # 'Aq'
    2 : 'HYD' , # 'Elements'
    3 : 'HYD', # 'SectMusk'
    4 : 'WATBAL' , # 'Cprod'
    5 : 'WATBAL' , # 'Elebu' 
    6 : 'NSAT' , # 'Nsat'
}

binfiles_type = {
    1 : ['MB', 'H'] , # 'Aq'
    2 : ['Q'] , # 'Elements'
    3 : ['Q'], # 'SectMusk'
    4 : ['MB'] , # 'Cprod'
    5 : ['MB'] , # 'Elebu' 
    6 : ['MB'] , # 'Nsat'
}



nbRecs = {
    'AQ_MB' : 16,
    'AQ_H' : 1,
    'HYD_Q' : 1,
    'HYD_H' : 2,
    'HYD_MB' : 9,
    'WATBAL_MB' : 10,
    'HDERM_Q' : 1,
    'HDERM_MB' : 9,
    'NONSAT_MB' : 4,
    }

paramRecs = {
    'WATBAL_MB' : [
        'rain',
        'etp',
        'runoff',
        'inf',
        'etr',
        'direct_sout',
        'stocksoil', 
        'stockruiss',
        'stockinf',
        'error'
    ],

    'HYD_Q' : [
        'discharge'
    ],

    'AQ_H' : [
        'piezhead'
    ]
        }

# DIALOG BOX CONFIG
## Dictionnary (key = compartment, value = correspond DialogBox)
dialog_box = {
    # "Settings" : "DialogSettings",
    "Watbal (Waterbalance)" : "DialogWatbal", 
    "Hyd (River Network)" : "DialogHyd",
    "Aq (Aquifer)" : "DialogAq",
    "Nsat (Unsatured)" : "DialogNsat"
} 

settings_compartment_id = {
    "checkAq" : 1,
    "checkHyd" : 2,
    "checkSurf" : 3, 
    "checkNsat" : 4, 
    

}

## TYPE OF FILE CAN BE IMPORTED TO USE THE PLUGIN
importedfilestypes = {
    "txt" : "Text (*.txt)", 
    "bin" : "Binaire (*.bin)",
    "shp" : "Shapefiles (*.shp)"
}

## SAVING PARAMETERS FORMATS FOR CAWAQS
CawSavingFormat = {
    1 : {
        'cols' : ['ID_INT', '']
    }
}

## OBS CONFIG 
# id_compartment : {"id_col" : id_col}
obs_config = {
    2 : {
        "id_col_time" : 1, 
        "id_col_data" : 3
        }
    }

## PARAMETRIZATION FILE 
paramInput = {
    'WATBAL' : {
        'classical' : {
            'NAME': str,
            'CRT': float, 
            'DCRT': float, 
            'R': float, 
            'FN': float, 
            'CQR': float, 
            'CQRMAX': float, 
            'CQI': float, 
            'CQIMAX': float, 
            'RNAP': float, 
        },
        'Infiltration excess' : {
            'NAME' : str,
            'CRT': float, 
            'DCRT': float, 
            'R': float, 
            'FN':float, 
            'CQR':float, 
            'CQRMAX':float, 
            'CQI':float, 
            'CQIMAX':float, 
            'RNAP':float,
            'RINF':str
        }
    }
}