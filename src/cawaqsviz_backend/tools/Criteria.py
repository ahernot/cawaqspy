import numpy as np

def averageSimObsRatio(sim_values, obs_values) :
    """
    Determine the average ratio between simulated values and observed values

    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    return np.nanmean(sim_values) / np.nanmean(obs_values)


def pbias(sim_values, obs_values):
    """
    Determine the average Pourcent Bias between simulated values and observed values
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """

    return np.nansum(sim_values - obs_values)/np.nansum(obs_values) * 100

def pbiasNormStD(sim_values, obs_values) : 
    bias = pbias(sim_values, obs_values)
    std  = standardDeviation(obs_values)

    return bias/std

def standardDeviation(values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    return np.sqrt(1/len(values) * np.nansum(values - np.nanmean(values)) ** 2)

def standardDeviationRatio(sim_values, obs_values) : 
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    a = standardDeviation(sim_values)
    b = standardDeviation(obs_values)

    return a/b

def correlationPearson(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    a = np.nansum((obs_values - np.nanmean(obs_values)) * (sim_values - np.nanmean(sim_values)))
    b = np.nansum((obs_values - np.nanmean(obs_values)) ** 2) * np.nansum((sim_values - np.nanmean(sim_values)) ** 2)


    return a/np.sqrt(b)



def kge(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """

    bias        = pbias(sim_values, obs_values)
    sDratio     = standardDeviationRatio(sim_values, obs_values)
    corr        = correlationPearson(sim_values, obs_values)

    return 1 - np.sqrt((corr - 1) ** 2 + (sDratio - 1) **2 + (bias -1) ** 2)



def nash(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    return 1 - (np.nansum((obs_values - sim_values) ** 2)) / (np.nansum(obs_values - [np.nanmean(obs_values)] * len(obs_values)) ** 2)



def rmse(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    n_obs = np.sum(ñp.isnan(obs_values))

    return np.sqrt((np.sum(obs_values - sim_values) **2) / n_obs )



def calcCritClassics(sim_values, obs_values) : 
    crits = {}

    crits['PBIAS'] = pbias(sim_values, obs_values)
    crits['AVERAGE SIM/OBS'] = averageSimObsRatio(sim_values, obs_values)

    return crits

def filterCritStat(crits : list) :
    """  
    Filters statistical criteria values to avoid 'np.nan' values. 
    Statistical criteria that could not be determined are replaced 
    by the value -9999.

    Parameters : 
        • crist : list of statistical criteria
    """  
    crits_filtred = []

    for crit in crits : 
        if isinstance(crit) : 
            print(f"Crit type : {type(crit)}")
            crits_filtred.append(-9999)
        else : 
            print(f"Crit type : {type(crit)}")
            crits_filtred.append(crit)

    return crits_filtred


    