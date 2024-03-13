from src.utils.format_command_file import format_command_dict


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
