
def convertDischarge(obs_values, obs_unit:str = 'l/s', verbose=False):
    """
    Convert Observation Matrix to Discharge CaWaQS Output (mm3/s)

    Parameters : 
        • obs_values : 1D obs Matrix
        • obs_unit : observation unit
    """

    if obs_unit == 'l/s' : 
        m = 1e-3

    elif obs_unit == 'm3/s' :
        m = 1

    if verbose: print(f"CONVERT OBS in {obs_unit} to m3/s")
    return [value * m for value in obs_values]

def convertWatbalVariable(sim_value:float, surf:float, wanted_unit:str):
    """
    Convert Sim values from watbal componante in wanted value for output values in 
    mm3/s (CaWaQS convention)

    Parameters : 
        • sim_values : 1D sim matrix
        • wanted_unit : out unit output (m3/s, l/s, mm/s)
        • surfs : 1D surface matrix (ordered by cells ids)
    """
    
    if wanted_unit == 'm3/j' : 
        m = 86400
    
    if wanted_unit == 'mm/j' : 
        m = 1/surf * 86400 * 1e3

    if wanted_unit == 'l/s' : 
        m = 1e-3

    return sim_value * m

    