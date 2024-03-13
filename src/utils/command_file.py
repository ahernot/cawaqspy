# from typing import Union
# class Unit:
#     def __init__ (self, val: Union[int, float], unit: str = None):
#         self
#     def __repr__ (self):
#         return self.val
# TODO: number with unit

# class Hydro:
#     def __init__ (self, name, **kwargs):
#         self.__name = name

# class Aquifer (Hydro):
#     def __init__ (self, name, **kwargs):
#         super().__init__(name, **kwargs)
    
#     def settings (self, **kwargs):
#         self.__settings = kwargs  # TODO

#     def add_gw_mesh_paths (self, **kwargs):
#         # tertiaire = "grid_TERT.txt", craie = "grid_CRAI.txt", jurassique = "grid_JURA.txt"
#         self.__gw_mesh_dict = {'layer': [
#             {f'{key} include {val}': None} for key, val in kwargs.items()
#         ]}
    
#     def add_setup_layers (self):
#         pass

# class Simulation:
#     def __init__ (self, name: str): pass
#     @classmethod
#     def from_dict (cls): pass
#     def to_dict (self): pass




class CommandFile:

    def __init__ (self, input_folders: list, output_folder: str):
        self.__input_folders = input_folders
        self.__output_folder = output_folder
        self.__simulation_dict = dict()
        self.__hydro_dict = dict()
        self.__outputs_dict = dict()
        
    def add_config (self, name: str, year_start, year_stop, dt, **kwargs):
        self.__name = name
        self.__year_start = year_start
        self.__year_stop = year_stop

        self.__simulation_dict = {
            '__inline__': name,
            'TIME': {
                'year_init': year_start,
                'year_end': year_stop,
                'dt': dt,
            },
            'SETTINGS': {  # TODO: from kwargs  # TODO: specify required arguments? dict merge?
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
        }

    def add_hydro_layer (self):
        raise NotImplementedError
    def add_hydro_layer_dict (self, name: str, layer_dict: dict):
        self.__hydro_dict [name] = layer_dict

    def add_output (
            self,
            name: str,
            format: str = 'UNFORMATTED',
            dt: str = '[d] 1',  # TODO: int with unit
            **kwargs
        ):
        """
        Add an output format to the command file.

        Args:
            name (str): Name of the output

        Kwargs:
            active (bool): Toggle layer activation (default: True)
            print_final_state (bool): Print final state
            spatial_scale (str): Spatial scale (example: 'WATBAL_ELEMENT')
        """

        # Initialize output entry
        self.__outputs_dict [name] = {
            'Output_settings': {
                '__inline__': kwargs.get('active', True),
                'format': format,
                'time': {f'dt = {dt}': None}
            }
        }

        # Add optional output settings
        if 'print_final_state' in kwargs.keys(): self.__outputs_dict [name]['Output_settings']['print_final_state'] = kwargs['print_final_state']
        if 'space_scale' in kwargs.keys(): self.__outputs_dict [name]['Output_settings']['spatial_scale'] = kwargs['spatial_scale']

    @property
    def command_dict (self) -> dict:
        command_dict = {
            'Input_folders': self.__input_folders,
            'Output_folder': self.__output_folder,
            'simulation': self.__simulation_dict,
            'HYDRO': {key: val for key, val in self.__hydro_dict.items()},
            'OUTPUTS': self.__outputs_dict
        }
        return command_dict

    @property
    def command_file (self) -> str:
        return print_command_dict(self.command_dict, indent_break_max=0)




def print_command_dict (command_dict: dict, indent_break_max = 0) -> str:
    """
    Recursively print the command dictionary in a human-readable format.

    Args:
        command_dict (dict): Command dictionary to print.
        indent_break_max (int): Maximum indentation level at which to print line breaks between elements (0 prints no breaks).
    
    Returns:
        str: Command file in string format
    """

    def __print_recur (
            subdict: dict,
            out_list: list = [],
            indent: int = 0,
            key_len_max: int = 0,
            indent_break_max: int = 0
        ) -> list:
        """
        _summary_

        Args:
            subdict (dict): Current subdict to print.
            out_list (list, optional): Current output list. Defaults to [].
            indent (int, optional): Current indent level. Defaults to 0.
            key_len_max (int, optional): Max key length for current subdict (for text formatting). Defaults to 0.
            indent_break_max (int, optional): Maximum indentation level at which to print line breaks between elements (0 prints no breaks). Defaults to 0.

        Returns:
            list: _description_
        """
        
        __types_single = (str, int, float, bool, type(None))
        __ichar = '\t'
        __iincr = 1

        def __serialize (x):
            if type(x) == bool:
                return 'YES' if x else 'NO'
            return x


        # Run through subdict's items
        for key, val in subdict.items():

            # Unpack subdicts
            if type(val) == dict:
                
                # Only one leaf (non-iterable value): compact writing (curly brackets on the same line)
                subitems = list(val.values())
                if len(subitems) == 1 and type(subitems[0]) in __types_single:
                    print_prefix = f'{__serialize(key)} '
                    print_suffix = f'= {{ {__serialize(list(val.keys())[0])} }}'
                    if key_len_max > len(print_prefix): print_prefix += ' ' * (key_len_max - len(print_prefix))
                    out_list.append (__ichar*indent + print_prefix + print_suffix)  # Print
                
                # Multiple subitems: expanded dict writing (recursive call) - no formatting adjustment with spaces
                else:
                    # Calculate key_len_max (ignore keys of expanded dicts and special keys)
                    keys_eligible_ = list()
                    for key_, val_ in val.items():
                        # Special keys
                        if key_ == '__inline__': continue
                        # Non-iterable values
                        if type(val_) in __types_single:
                            keys_eligible_.append(key_)
                        # Single-element dict values
                        elif type(val_) == dict:
                            subitems = list(val_.values())
                            if len(subitems) == 1 and type(subitems[0]) in __types_single:
                                keys_eligible_.append(key_)
                    key_len_max_ = max([len(key) for key in keys_eligible_]) + 1 if keys_eligible_ else 0

                    out_list.append (__ichar*indent + f'{__serialize(key)} = {{')
                    out_list = __print_recur(val, out_list=out_list, indent=indent+__iincr, key_len_max=key_len_max_)
                    out_list.append (__ichar*indent + '}')


            # Unpack lists to assign the key to each subdictionary
            elif type(val) == list:
                # List contains only non-iterable elements (only print key once)
                if all((type(v) in __types_single  for v in val)):
                    print_prefix = f'{__serialize(key)} '
                    out_list.append (__ichar*indent + print_prefix + f'= {val[0]}')
                    for item in val[1:]:
                        out_list.append (__ichar*indent + ' '*len(print_prefix) + f'= {item}')

                # List contains dictionary elements
                else:
                    for item in val:
                        out_list = __print_recur({key: item}, out_list=out_list, indent=indent)  # Distribute print_recur across all subdicts contained in the list


            # End node (leaf)
            else:
                # Inline text (prints value only, formatted as "value") for elements of dict with '__inline__' key
                if key == '__inline__':
                    out_list.append (__ichar*indent + __serialize(val))

                # Regular key-pair formatted as "key = value"
                else:
                    print_prefix = f'{__serialize(key)} '
                    print_suffix = f'= {__serialize(val)}'
                    if key_len_max > len(print_prefix): print_prefix += ' ' * (key_len_max - len(print_prefix))
                    out_list.append (__ichar*indent + print_prefix + print_suffix )
            

            # Line break between main sections
            if indent < indent_break_max:
                out_list.append ('')

        return out_list
    
    return '\n'.join( __print_recur(command_dict, out_list=[], indent=0, key_len_max=0, indent_break_max=indent_break_max) )



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
            'OMP': {'NO nthreads': 8},  # TODO
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


