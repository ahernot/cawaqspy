import os
import numpy as np

from src.cawaqsviz_backend.parameters import *
from src.cawaqsviz_backend.ExploreData import ExploreData
from src.cawaqsviz_backend.tools.Criteria import *  # pbias, etc



class StatisticalCriteria: 

    def __init__ (self, exd: ExploreData):

        # Load global instance of ExploreData
        self.exd = exd

        # Parameters
        self.obstype = 'Discharge'  # 'Hydraulic Head'
        self.unit = 'l/s'  # ['l/s', 'm3/s']


        #! TODO: needed? or for txt file
        # check and creat StatCrit repertory if it doesn't exit
        # self.directoryStatCrit = os.path.join(self.exd.post_process_directory, 'STATS_CRITS')
        # self.makeDirectory(self.directoryStatCrit)


    def run (self, verbose=False) -> dict:

        # Get obs (resolution &) output type
        id_compartment, outtype, param = self.getSimObsResolutionOutputType()
        compartment = self.exd.compartments[id_compartment]

        # Read Sim and Obs Data, calculate Perf stats and Add CRIT Layer in the current projet
        stats_dict = dict()
        for obs_point in compartment.obs.obs_points:
            
            if verbose: print(f'\nObservation name point {obs_point.name}')
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
                tempDirectory = self.exd.temp_directory,
                obs_unit    = self.unit
            )

            # Calculate performance (biases, etc.)
            crits = self.calcPerfStats(simobsdf['sim'].values, simobsdf['obs'].values)
            stats_dict[obs_point.name] = crits

        return stats_dict
        

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
        crits['avg_obs'] = float(np.nanmean(obs_data))
        crits['avg_sim'] = float(np.nanmean(sim_data))
        crits['std_obs'] = float(np.nanstd(obs_data))
        crits['std_sim'] = float(np.nanstd(sim_data))
        crits['n_obs'] = countNObservation(obs_data)

        # Compute statistical criteria for data
        crits['stack_couples'] = float(stackCouples(sim_data, obs_data))
        crits['sim_obs_ratio_avg'] = float(averageSimObsRatio(sim_data, obs_data))
        crits['bias'] = float(bias(sim_data, obs_data))
        crits['pbias'] = float(pbias(sim_data, obs_data))
        crits['pbias_norm_std'] = float(pbiasNormStD(sim_data, obs_data))
        crits['std_ratio'] = float(standardDeviationRatio(sim_data, obs_data))
        crits['pearson_correlation'] = float(correlationPearson(sim_data, obs_data))
        crits['kge'] = float(kge(sim_data, obs_data))
        crits['nash'] = float(nash(sim_data, obs_data))
        crits['rmse'] = float(rmse(sim_data, obs_data))

        return crits
