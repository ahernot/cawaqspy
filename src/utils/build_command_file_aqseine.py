from src.config import *


# Default variables
PARAMS_DICT = {
    'dirpath_data': '/home/anatole/Documents/DATA_CAWAQS/SEINE_3C/DATA_SEINE_SIMPLE',
    'dirpath_output': '/home/anatole/Documents/DATA_CAWAQS_OUT/TestProj',
    'n_threads': 8,
    'donsur': 'donsur_BU28.txt',
    'lien_bu_mto': 'LIEN_BU28_MTO.txt'
}


# Command file template (contains some hard-coded values)
COMMFILE = """\
Input_folders   = {dirpath_data}/Cmd_files
                = {dirpath_data}/DATA_HYD
                = {dirpath_data}/DATA_SURF
                = {dirpath_data}/DATA_NSAT
                = {dirpath_data}/DATA_MESH
                = {dirpath_data}/DATA_AQ
                = {dirpath_data}/DATA_AQ/Heterogeneous
				
Output_folder   = {dirpath_output}

simulation = {{ 

    SEINE_SIMPLE

    TIME = {{ 
        year_init = {year_start}
        year_end  = {year_stop}
        dt        = [d] 1.
    }}

    SETTINGS = {{
        transport   = NO
        type        = transient
        eps_Q       = [m3/s] 0.000001
        eps_Z       = [m] 0.00001
        theta       = 1.0
        nit_pic_max = 1            
        eps_pic     = [cm] 15
        print_surf  = YES
        debug       = NO
    }}
}}

HYDRO = {{


    AQUIFER = {{

        SETTINGS = {{ 
            anisotropy_factor = 0.1                 # facteur d'anisotropie verticale     
            # specific_yield_factor = 0.01            # facteur de conversion S d'UNCONFINED vers CONFINED
            log_fluxes = NO                         # Bilan de flux à l'échelle de la couche
            print_lithos = NO                       # Map des lithos affleurantes (si en mode UNCONFINED)
        }} 

        OMP = {{ NO nthreads = {n_threads} }}

        GW_MESH = {{
            layer = {{ tertiaire   include grid_TERT.txt }}     
            layer = {{ craie       include grid_CRAI.txt }}     
            layer = {{ jurassique  include grid_JURA.txt }}     
        }}

        SET_UP = {{
 
            setup_layer = {{                   
                tertiaire
                param = {{
                    transm_homo    = {{ include Transm_HET_TERT.txt }}  
                    # transm_homo    = {{ uniform 1.12E-2 [m2/s] }}        # Transmissivités uniformes
                    # transm_homo    = {{ 5.E-6 include Thickness_TERT.txt }}   # Définition de la valeur de permeabilité sous jacente basée sur épaisseur
  
                    storage 	   = {{ include Emmag_HET_TERT.txt }}      # pond 0.2   
  
                    h_ini 		   = {{ include H_ini_HET_TERT.txt }}        
                    thick 		   = {{ include Thickness_HET_TERT.txt }}
		    
                    conductance    = {{ include Cond_TOP_noRIV_TERT.txt }}  # Calcul de conductance automatique         
                    # conductance    = {{ 1.E-5 include Cond_drain_TERT.txt }}   # Calcul de conductance pondérée  # pas de conductance devrait correspondre à une absence de débordement et à une mise en charge de l'aquifère
	       
                    Mean 		   = HARMONIC
                }}
                boundary 		   = {{ include Bound_TERT.txt }}           
            }}
 
            setup_layer = {{
                craie
                param = {{
                    transm_homo    = {{ include Transm_HET_CRAI.txt }}   # transmissivité en m^2/s; perméabilité en m/s
                   # transm_homo    = {{ uniform 3.52E-2 [m2/s] }} 
                   # transm_homo    = {{ 1.E-4 include Thickness_CRAI.txt }}  # facteur = perméabilité, * thickness = transm
		   
                    storage 	   = {{ include Emmag_HET_CRAI.txt }}    #pond 0.2
		   
                    h_ini 		   = {{ include H_ini_HET_CRAI.txt }}         
                    thick 		   = {{ include Thickness_HET_CRAI.txt }}
                                
                    conductance    = {{ include Cond_TOP_noRIV_CRAI.txt }}
                    # conductance    = {{ 1.E-5  include Cond_drain_CRAI.txt }}   
		    
                    Mean 		   = HARMONIC
                }}
                boundary 		   = {{ include Bound_CRAI.txt }}            
            }}
 
            setup_layer = {{
                jurassique
                param = {{  
                    transm_homo    = {{ include Transm_HET_JURA.txt }}
		            # transm_homo    = {{ uniform 2.20E-2 [m2/s] }} 
                    # transm_homo    = {{ 1.E-5 include Thickness_JURA.txt }}
		   
                    storage 	   = {{ include Emmag_HET_JURA.txt }}    #pond 0.6
		    
                    h_ini 		   = {{ include H_ini_HET_JURA.txt }}         
                    thick 		   = {{ include Thickness_HET_JURA.txt }}
		    
                    conductance    = {{ include Cond_TOP_noRIV_JURA.txt }}        
                    # conductance    = {{ 1.E-5 include Cond_drain_JURA.txt }}       
                    Mean 		   = HARMONIC
                }}
                boundary 		   = {{ include Bound_JURA.txt }}                           
            }}
        }} 
                    transm_homo    = {{ uniform 1.12E-2 [m2/s] }}        
    }} 


    SURFACE = {{

        MTO = {{
            mto_path     = {dirpath_data}/METEO      # --> Updated to 31/07/2023
            rain_prefix  = precip
            etp_prefix   = etp
            format       = UNFORMATTED
            mto_cell     = {{ include MTO_CELLS.txt }}
        }}

        WATER_BALANCE_UNIT = {{

            OMP = 	{{ YES NTHREADS = {n_threads} }}

            param        = {{ include {donsur} }}
            BU           = {{ include {lien_bu_mto} }}
            Cprod        = {{ include LIEN_ELE_BU_CPROD.txt }}

            catchments   = {{ 
                {{   1 Seine
                    Tc = [d] 17
                    include LISTE_CPROD_SEINE.txt }}
            }}

            Cprod_no_aq  = {{ include LIEN_CPROD_BU_NO_AQ.txt }}
            Cprod_aq     = {{ include LIEN_CPROD_AQ.txt }}

        }}

        NETWORK_DESCRIPTION = {{

            settings = {{
                ndim                = 1
                calculate_curvature = NO
                dx                  = [m] 0
                dz                  = [m] 10
                upstream_Hmin       = [m] 0.
                downstream_Hmax     = [m] 10.
                schem_type          = MUSKINGUM
                K_DEF               = TTRA
            }}

            OMP = 	{{ NO NTHREADS = {n_threads} }}

            network_musk   = {{ include NETWORK_MUSK.txt }}
            elements_musk  = {{ include ELEMENTS_MUSK.txt }}
        }} 

    }}

    NONSAT = {{  

         OMP = 	{{ NO NTHREADS = {n_threads} }}

         param      = {{ include PARAM_NSAT.txt }} 
         nsat_units = {{ include LIEN_NSAT_PARAM.txt }}        # Zonage uniforme à 0 res. (= Nsat inactif.)
         nsat_prod  = {{ include LIEN_NSAT_ELE_BU.txt }}
         nsat_aq    = {{ include LIEN_NSAT_AQF.txt }}           
    }}

}} # Fin du bloc HYDRO


OUTPUTS = {{

    MB_AQ = {{
    Output_settings = {{ NO
                        format = UNFORMATTED
                        print_final_state = YES
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    H_AQ = {{
    Output_settings = {{ YES
                        format = UNFORMATTED
                        print_final_state = YES
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    Q_HYD = {{
    Output_settings = {{ YES
                        format = UNFORMATTED
                        print_final_state = YES
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    H_HYD = {{
    Output_settings = {{ NO
                        format = UNFORMATTED
                        print_final_state = YES
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    MB_HYD = {{
    Output_settings = {{ NO
                        format = UNFORMATTED
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    NSAT = {{
    Output_settings = {{ NO
                        format = UNFORMATTED
                        time = {{ dt = [d] 1 }}
                      }}
    }}

    WATBAL = {{
    Output_settings = {{ YES
                        format = UNFORMATTED
                        time = {{ dt = [d] 1 }}
                        spatial_scale = WATBAL_ELEMENT
                     }}                   
    }}

}} # Fin du bloc OUTPUTS
"""



def build_command_file (path: str, **kwargs):

    # Generate command file from template
    params_dict = PARAMS_DICT.copy()
    params_dict.update(kwargs)
    commfile = COMMFILE.format(**params_dict)
    
    # Write to file
    with open(path, 'w', encoding='utf-8') as file:
        file.write(commfile)

    # Print success message
    verbose = kwargs.get('verbose', False)
    if verbose:
        print(f'Built command file in path "{path}"')