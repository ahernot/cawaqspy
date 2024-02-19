import os
import numpy as np

from src.cawaqsviz_backend.parameters import *
from src.cawaqsviz_backend.ExploreData import ExploreData
from src.cawaqsviz_backend.tools.Criteria import pbias  # , averageSimObsRatio



class StatisticalCriteria: 

    def __init__ (self, exd: ExploreData):

        # Load global instance of ExploreData
        self.exd = exd

        # Parameters
        self.calc_pbias = True
        self.check_average_simobs = False
        self.obstype = 'Discharge'  # ['', 'Discharge', 'Hydraulic Head']
        self.unit = 'l/s'  # ['l/s', 'm3/s']


        #! TODO: needed? or for txt file
        # check and creat StatCrit repertory if it doesn't exit
        self.directoryStatCrit = os.path.join(self.exd.post_process_directory, 'STATS_CRITS')
        self.makeDirectory(self.directoryStatCrit)


    def run (self) -> dict:

        # Get obs (resolution &) output type
        id_compartment, outtype, param = self.getSimObsResolutionOutputType()
        compartment = self.exd.compartments[id_compartment]

        # Read Sim and Obs Data, Calc Perf stats and Add CRIT Layer in the current projet
        pbiases_dict = dict()
        for obs_point in compartment.obs.obs_points:
            
            print(f'\nObservation name point {obs_point.name}')
            simobsdf = self.exd.manage.Temporal().readSimObs(
                compartment = compartment,
                outtype     = outtype,  # 'Q' (discharge)
                param       = param,  # 'discharge
                obs_point   = obs_point, 
                simstart    = self.exd.startsim,
                endsim      = self.exd.endsim,
                cutstart    = '2006-08-01',  # TODO
                cutend      = '2023-07-31',  # TODO
                id_col_data = obs_config[id_compartment]['id_col_data'],  # From parameters.py
                id_col_time = obs_config[id_compartment]['id_col_time'],  # From parameters.py
                id_parameter = paramRecs[compartment.compartment + '_' + outtype].index(param),  # From parameters.py
                tempDirectory = self.exd.temp_directory,  # TODO: create temp dir
                obs_unit    = self.unit
            )

            # Calculate performance (biases, etc.)
            crits = self.calcPerfStats(simobsdf['sim'].values, simobsdf['obs'].values)
            pbiases_dict[obs_point.name] = crits

        return pbiases_dict
        

    def getSimObsResolutionOutputType (self):
        # get Observation Resolution 
        if self.obstype == 'Discharge': 
            id_compartment  = reversed_module_caw['HYD']
            outtype         = 'Q'
            param           = 'discharge'

        elif self.obstype == 'Hydraulic Head': 
            id_compartment      = reversed_module_caw['AQ']
            outtype             = 'H'
            param               = 'piezhead'
        
        return id_compartment, outtype, param


    def calcPerfStats (self, sim_data, obs_data):
        """
        Calculate performance stats
        """

        # Initialize crits dictionary
        crits = dict()
        crits['AObs'] = float(np.nanmean(obs_data))
        crits['ASim'] = float(np.nanmean(sim_data))
        crits['StdObs'] = float(np.nanstd(obs_data))
        crits['StdSim'] = float(np.nanstd(sim_data))

        # Compute pbias
        if self.calc_pbias:
            crits['PBIAS'] = float(pbias(sim_data, obs_data))

        # Compute average sim/obs
        if self.check_average_simobs:
            raise NotImplementedError('Only pbias is available to calculate')
            crits['AVERAGE OBS/SIM'] = float(averageSimObsRatio(sim_data, obs_data))

        return crits
