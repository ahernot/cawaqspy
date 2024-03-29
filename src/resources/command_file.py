from src.utils.format_command_file import format_command_dict
from typing import Union
from src.utils.format import format_quantity

try:
    from pint import Quantity
except ImportError:
    # Define a dummy Quantity class if pint is not installed
    class Quantity:
        pass



class CommandFileElement:
    def __init__ (self, name: str):
        self.name = name
    @property
    def dict (self) -> dict:
        raise NotImplementedError


class Hydro (CommandFileElement):  # TODO: deprecated
    """ Structure for the HYDRO element of the command file """
    def __init__ (self):
        raise DeprecationWarning
        super().__init__(name='HYDRO')
        self.__elements_dict = dict()
    
    @property
    def dict (self) -> dict:
        return {name: element.dict for (name, element) in self.__elements_dict.items()}

    def add_element (self, element: CommandFileElement):  # TODO: specify type as child type
        self.__elements_dict [element.name] = element

class HydroAquifer (CommandFileElement):
    """ Aquifer-specific structure for the HYDRO element of the command file. """
    def __init__ (self):
        super().__init__(name='AQUIFER')
        self.__settings_dict = dict()
        self.__omp_dict = dict()
        self.__gw_mesh_dict = {'layer': list()}
        self.__set_up_dict = {'setup_layer': list()}

    @property
    def dict (self) -> dict:
        command_dict = {
            'SETTINGS': self.__settings_dict,
            'OMP': self.__omp_dict,
            'GW_MESH': self.__gw_mesh_dict,
            'SET_UP': self.__set_up_dict
        }
        return command_dict

    def write_settings (self, **settings):
        self.__settings_dict = settings
    def write_omp (self, val: bool = False, n_threads: int = 8):
        val_str = 'YES' if val else 'NO'
        self.__omp_dict = {f'{val_str} nthreads': n_threads}

    def add_layer (
            self,
            name: str,
            path_gw_mesh: str,
            path_transm_homo: str,
            path_storage: str,
            path_h_ini: str,
            path_thick: str,
            path_conductance: str,
            path_boundary: str,
            mean: str = 'HARMONIC'
        ):
        
        # Add GW_MESH
        self.__gw_mesh_dict['layer'] .append({f'{name} include {path_gw_mesh}': None})

        # Add SET_UP
        layer_setup_dict = {
            '__inline__': name,
            'param': {
                'transm_homo': {f'include {path_transm_homo}': None},
                'storage': {f'include {path_storage}': None},
                'h_ini': {f'include {path_h_ini}': None},
                'thick': {f'include {path_thick}': None},
                'conductance': {f'include {path_conductance}': None},
                'Mean': mean,
            },
            'boundary': {f'include {path_boundary}': None},
        }
        self.__set_up_dict['setup_layer'] .append(layer_setup_dict)

class HydroSurface (CommandFileElement):
    """ Surface-specific structure for the HYDRO element of the command file. """
    def __init__ (self):
        super().__init__(name='SURFACE')
        self.__mto_dict = dict()
        self.__wbu_dict = dict()
        self.__network_description_dict = dict()

    @property
    def dict (self) -> dict:
        command_dict = {
            'MTO': self.__mto_dict,
            'WATER_BALANCE_UNIT': self.__wbu_dict,
            'NETWORK_DESCRIPTION': self.__network_description_dict,
        }
        return command_dict
    
    # Weather
    def write_mto (
            self,
            path_mto: str,
            path_mto_cell: str,
            prefix_rain: str = 'precip',
            prefix_etp: str = 'etp',
            format_: str = 'UNFORMATTED'
        ):
        self.__mto_dict = {
            'mto_path': path_mto,
            'rain_prefix': prefix_rain,
            'etp_prefix': prefix_etp,
            'format': format_,
            'mto_cell': {f'include {path_mto_cell}': None},
        }

    # Water balance unit
    def write_wbu (
            self,
            catchments: str,
            path_donsur: str,
            path_bu_mto: str,
            path_cprod: str,
            path_cprod_aq: str,
            path_cprod_no_aq: str,
            val_omp: bool = True,
            n_threads: int = 8
        ):
        omp_val_str = 'YES' if val_omp else 'NO'
        self.__wbu_dict = {
            'OMP': {f'{omp_val_str} nthreads': n_threads},
            'param': {f'include {path_donsur}': None},
            'BU': {f'include {path_bu_mto}': None},
            'Cprod': {f'include {path_cprod}': None},
            'catchments': {catchments: None},
            'Cprod_no_aq': {f'include {path_cprod_no_aq}': None},
            'Cprod_aq': {f'include {path_cprod_aq}': None},
        }

    # Network Description
    def write_network_description (
            self,
            path_network_musk: str,
            path_elements_musk: str,
            ndim: int = 1,
            calculate_curvature: bool = False,
            dx: Union[str, int, float, Quantity] = '[m] 0',
            dz: Union[str, int, float, Quantity] = '[m] 10',
            upstream_hmin: Union[str, int, float, Quantity] = '[m] 0.',
            downstream_hmax: Union[str, int, float, Quantity] = '[m] 10.',
            schem_type: str = 'MUSKINGUM',
            k_def: str = 'TTRA',
            val_omp: bool = False,
            n_threads: int = 8
        ):

        # Format quantities
        if isinstance(dx, Quantity): dx = format_quantity(dx, type_=int)  # Formatted as int
        if isinstance(dz, Quantity): dz = format_quantity(dz, type_=int)  # Formatted as int
        if isinstance(upstream_hmin, Quantity): upstream_hmin = format_quantity(upstream_hmin, type_=float)  # Formatted as float
        if isinstance(downstream_hmax, Quantity): downstream_hmax = format_quantity(downstream_hmax, type_=float)  # Formatted as float

        omp_val_str = 'YES' if val_omp else 'NO'
        self.__network_description_dict = {
            'settings': {
                    'ndim': ndim,
                    'calculate_curvature': calculate_curvature,
                    'dx': dx,
                    'dz': dz,
                    'upstream_Hmin': upstream_hmin,
                    'downstream_Hmax': downstream_hmax,
                    'schem_type': schem_type,
                    'K_DEF': k_def,
                },
            'OMP': {f'{omp_val_str} nthreads': n_threads},
            'network_musk': {f'include {path_network_musk}': None},
            'elements_musk': {f'include {path_elements_musk}': None}
        }

class HydroNonSat (CommandFileElement):
    """ Surface-specific structure for the NONSAT element of the command file. """
    def __init__ (self):
        super().__init__(name='NONSAT')
        self.__mto_dict = dict()
        self.__wbu_dict = dict()
        self.__network_description_dict = dict()

    @property
    def dict (self) -> dict:
        return self.__settings_dict

    def write_settings (
            self,
            path_param: str,
            path_nsat_units: str,
            path_nsat_prod: str,
            path_nsat_aq: str,
            val_omp: bool = False,
            n_threads: int = 8
        ):
        omp_val_str = 'YES' if val_omp else 'NO'
        self.__settings_dict = {
            'OMP': {f'{omp_val_str} nthreads': n_threads},
            'param': {f'include {path_param}': None},
            'nsat_units': {f'include {path_nsat_units}': None},
            'nsat_prod': {f'include {path_nsat_prod}': None},
            'nsat_aq': {f'include {path_nsat_aq}': None},     
        }


class CommandFile:

    def __init__ (self, input_folders: list, output_folder: str):
        # Save IO folders
        self.__input_folders = input_folders
        self.__output_folder = output_folder

        # Initialize subdicts
        self.__simulation_dict = dict()
        self.__hydro_dict = dict()
        self.__outputs_dict = dict()
        
    def add_config (
            self,
            name: str,
            year_start: int,
            year_stop: int,
            dt: Union[str, int, float, Quantity],
            transport: bool = False,
            type_: str = 'transient',
            eps_Q: Union[str, int, float, Quantity] = '[m3/s] 0.000001',  # TODO: Quantity
            eps_Z: Union[str, int, float, Quantity] = '[m] 0.00001',  # TODO: Quantity
            eps_pic: Union[str, int, float, Quantity] = '[cm] 15',  # TODO: Quantity
            theta: Union[int, float] = 1.0,
            nit_pic_max: int = 1,
            print_surf: bool = False,
            debug: bool = False,
            **kw_settings
        ):

        # Save main values
        self.name = name
        self.year_start = year_start
        self.year_stop = year_stop

        # Serialize quantities  # TODO: implement for eps_*
        if isinstance(dt, Quantity): dt = format_quantity(dt, type_=int)  # Formatted as int
        elif isinstance(dt, (int, float)): dt = f'[d] {dt}'  # Default unit is days  # TODO: specific serialization function for the CommandFile constructors

        self.__simulation_dict = {
            '__inline__': name,
            'TIME': {
                'year_init': year_start,
                'year_end': year_stop,
                'dt': dt,
            },
            'SETTINGS': {
                'transport': transport,
                'type': type_,
                'eps_Q': eps_Q,  
                'eps_Z': eps_Z,
                'theta': theta,
                'nit_pic_max': nit_pic_max,
                'eps_pic': eps_pic,
                'print_surf': print_surf,
                'debug': debug,
            }
        }
        
        # Apply kwargs (if any) – overwrites SETTINGS values
        self.__simulation_dict['SETTINGS'] .update(kw_settings)
    
    def __repr__ (self) -> str:
        return f'Command file for {self.name} ({self.year_start} – {self.year_stop})'

    def add_hydro_layer (self):
        raise NotImplementedError
    def add_hydro_layer_dict (self, name: str, layer_dict: dict):
        self.__hydro_dict [name] = layer_dict

    def add_output (
            self,
            name: str,
            format: str = 'UNFORMATTED',
            dt: Union[str, int, float, Quantity] = '[d] 1',
            **kwargs
        ):
        """
        Add an output format to the command file.

        Args:
            name (str): Name of the output
            format (str): Format of the output (default: 'UNFORMATTED')
            dt (Union[str, int, float, Quantity]): Time step, in days (default: '[d] 1')

        Kwargs:
            active (bool): Toggle layer activation (default: True)
            print_final_state (bool): Print final state
            spatial_scale (str): Spatial scale (example: 'WATBAL_ELEMENT')
        """

        if isinstance(dt, Quantity): dt = format_quantity(dt, type_=int)  # Formatted as int
        elif isinstance(dt, (int, float)): dt = f'[d] {dt}'  # Default unit is days

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
        return format_command_dict (self.command_dict, indent_break_max=0)
    def build_command_file (self, indent_break_max: int = 0) -> str:
        return format_command_dict (self.command_dict, indent_break_max=indent_break_max)
