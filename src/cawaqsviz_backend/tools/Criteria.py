import numpy as np
import hydroeval as he

def countNObservation(obs_values) : 
    return np.sum(np.isnan(obs_values))

def stackCouples(sim_values, obs_values) : 
    mask = ~np.isnan(sim_values) & ~np.isnan(obs_values)

    stack = np.column_stack((sim_values[mask], obs_values[mask]))

    sim_values = stack[:,0]
    obs_values = stack[:,1]

    return sim_values, obs_values

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

def bias(sim_values, obs_values):
    """
    Determine the average Bias (%) between simulated values and observed values
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """

    return np.nansum(sim_values) / np.nansum(obs_values)

def pbias(sim_values, obs_values):
    """
    Determine the Bias (%) between simulated values and observed values
  
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

    return a / b

def correlationPearson(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    sim_values, obs_values = stackCouples(sim_values, obs_values)

    sim_mean = np.nanmean(sim_values)
    obs_mean = np.nanmean(obs_values)

    covar = np.nansum((sim_values - sim_mean) * (obs_values - obs_mean))
    devn  = np.sqrt(
        np.nansum((sim_values - sim_mean) ** 2 
                  * (np.nansum(obs_values - obs_mean)) ** 2)
                  )

    r = covar / devn

    return r


def kge(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """

    # bias        = gbias(sim_values, obs_values)
    # sDratio     = standardDeviationRatio(sim_values, obs_values)
    # corr        = correlationPearson(sim_values, obs_values)

    # return 1 - np.sqrt((corr - 1) ** 2 + (sDratio - 1) **2 + (bias -1) ** 2)
    
    sim_values, obs_values = stackCouples(sim_values, obs_values)
    kge_, r, alpha, beta = he.kge(sim_values, obs_values)

    return kge_[0]


def nash(sim_values, obs_values):
    """
  
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """

    sim_values, obs_values = stackCouples(sim_values, obs_values)


    # up_term = np.nanmean(sim_values - obs_values) ** 2
    # low_term = np.nanmean(obs_values - np.nanmean([obs_values]*len(obs_values))) ** 2

    # return 1 - (up_term - low_term)

    
    nash = he.nse(sim_values, obs_values)

    return nash


def rmse(sim_values, obs_values):
    """
    Rertun Root Mean Square criteria
    Parameters : 
        • sim_values : array 1D of simulated values
        • obs_values : array 1D of simulated values

    /!\ sim_values and obs_values should have the same length. If any value 
        has been record during a periode simulated, obs value should be 
        np.nan value 
    """
    # n_obs = countNObservation(obs_values)

    # return np.sqrt((np.nanmean(obs_values - sim_values) **2) / n_obs)
    sim_values, obs_values = stackCouples(sim_values, obs_values)
    rmse = he.rmse(sim_values, obs_values)

    return rmse

def calcCritClassics(sim_values, obs_values) : 
    crits = {}

    crits['Nobs']   = countNObservation(obs_values)
    crits['PBIAS']  = pbias(sim_values, obs_values)
    crits['AVERAGE SIM/OBS'] = averageSimObsRatio(sim_values, obs_values)
    crits['KGE']    = kge(sim_values, obs_values)
    crits['NASH']   = nash(sim_values, obs_values)
    crits['RMSE']   = rmse(sim_values, obs_values)

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
