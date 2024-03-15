COMMAND_DICT_SAMPLE = {

    'Input_folders': [
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/Cmd_files',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_HYD',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_SURF',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_NSAT',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_MESH',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_AQ',
        '/data/DATA/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/DATA_AQ/Heterogeneous'
    ],

    'Output_folder': '/data/DATA/DATA_CAWAQS_OUT/TestProj',

    'simulation': {
        '__inline__': 'SEINE_SIMPLE',
        'TIME': {
            'year_init': 2000,
            'year_end': 2010,
            'dt': '[d] 1.',
        },
        'SETTINGS': {
            'transport': False,
            'type': 'transient',
            'eps_Q': '[m3/s] 0.000001',
            'eps_Z': '[m] 0.00001',
            'theta': 1.0,
            'nit_pic_max': 1,
            'eps_pic': '[cm] 15',
            'print_surf': True,
            'debug': False,
        }
    },

    'HYDRO': {
        'AQUIFER': {
            'SETTINGS': {
                'anisotropy_factor': 0.1,
                'log_fluxes': False,
                'print_lithos': False,
            },
            'OMP': {'NO nthreads': 8},
            'GW_MESH': {
                'layer': [
                    {'tertiaire   include grid_TERT.txt': None},
                    {'craie       include grid_CRAI.txt': None},
                    {'jurassique  include grid_JURA.txt': None},
                ]
            }, 

            'SET_UP': {
                'setup_layer': [

                    # setup_layer 1
                    {
                        '__inline__': 'tertiaire',
                        'param': {
                            'transm_homo': {'include Transm_HET_TERT.txt': None},
                            'storage':     {'include Emmag_HET_TERT.txt': None},
                            'h_ini':       {'include H_ini_HET_TERT.txt': None},
                            'thick':       {'include Thickness_HET_TERT.txt': None},
                            'conductance': {'include Cond_TOP_noRIV_TERT.txt': None},
                            'Mean': 'HARMONIC',
                        },
                        'boundary': {'include Bound_TERT.txt': None},
                    },
            
                    # setup_layer 2
                    {
                        '__inline__': 'craie',
                        'param': {
                            'transm_homo': {'include Transm_HET_CRAI.txt': None},
                            'storage':     {'include Emmag_HET_CRAI.txt': None},
                            'h_ini':       {'include H_ini_HET_CRAI.txt': None},
                            'thick':       {'include Thickness_HET_CRAI.txt': None},
                            'conductance': {'include Cond_TOP_noRIV_CRAI.txt': None},
                            'Mean': 'HARMONIC',
                        },
                        'boundary': {'include Bound_CRAI.txt': None},
                    },

                    # setup_layer 3
                    {
                        '__inline__': 'jurassique',
                        'param': {
                            'transm_homo': {'include Transm_HET_JURA.txt': None},
                            'storage':     {'include Emmag_HET_JURA.txt': None},
                            'h_ini':       {'include H_ini_HET_JURA.txt': None},
                            'thick':       {'include Thickness_HET_JURA.txt': None},
                            'conductance': {'include Cond_TOP_noRIV_JURA.txt': None},
                            'Mean':        'HARMONIC',
                        },
                        'boundary': {'include Bound_JURA.txt': None},
                    },

                ]
            },
        },

        'SURFACE': {
            'MTO': {
                'mto_path': '/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE/METEO',
                'rain_prefix': 'precip',
                'etp_prefix': 'etp',
                'format': 'UNFORMATTED',
                'mto_cell': {'include MTO_CELLS.txt': None},
            },

            'WATER_BALANCE_UNIT': {
                'OMP': {'YES nthreads': 8},
                'param': {'include DONSUR_BU28.txt': None},
                'BU': {'include LIEN_BU28_MTO.txt': None},
                'Cprod': {'include LIEN_ELE_BU_CPROD.txt': None},
                'catchments': {'{ 1 Seine\nTc = [d] 17\ninclude LISTE_CPROD_SEINE.txt }': None},
                'Cprod_no_aq': {'include LIEN_CPROD_BU_NO_AQ.txt': None},
                'Cprod_aq': {'include LIEN_CPROD_AQ.txt': None},
            },

            'NETWORK_DESCRIPTION': {
                'settings': {
                    'ndim': 1,
                    'calculate_curvature': False,
                    'dx': '[m] 0',
                    'dz': '[m] 10',
                    'upstream_Hmin': '[m] 0.',
                    'downstream_Hmax': '[m] 10.',
                    'schem_type': 'MUSKINGUM',
                    'K_DEF': 'TTRA',
                },
                'OMP': {'NO nthreads': 8},
                'network_musk': {'include NETWORK_MUSK.txt': None},
                'elements_musk': {'include ELEMENTS_MUSK.txt': None},
            }
        },

        'NONSAT': {  
            'OMP': {'NO nthreads': 8},
            'param': {'include PARAM_NSAT.txt': None},
            'nsat_units': {'include LIEN_NSAT_PARAM.txt': None},
            'nsat_prod': {'include LIEN_NSAT_ELE_BU.txt': None},
            'nsat_aq': {'include LIEN_NSAT_AQF.txt': None},           
        },
    },

    'OUTPUTS': {
        'MB_AQ': {
            'Output_settings': {
                '__inline__': False,
                'format': 'UNFORMATTED',
                'print_final_state': True,
                'time': {'dt = [d] 1': None},
            }
        },
        'H_AQ': {
            'Output_settings': {
                '__inline__': True,
                'format': 'UNFORMATTED',
                'print_final_state': False,
                'time': {'dt = [d] 1': None},
            }
        },
        'Q_HYD': {
            'Output_settings': {
                '__inline__': True,
                'format': 'UNFORMATTED',
                'print_final_state': False,
                'time': {'dt = [d] 1': None},
            }
        },
        'NSAT': {
            'Output_settings': {
                '__inline__': False,
                'format': 'UNFORMATTED',
                'time': {'dt = [d] 1': None},
            }
        },
        'WATBAL': {
            'Output_settings': {
                '__inline__': True,
                'format': 'UNFORMATTED',
                'time': {'dt = [d] 1': None},
                'spatial_scale': 'WATBAL_ELEMENT',
            }
        },
    },
}
