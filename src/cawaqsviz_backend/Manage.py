import os 
from os import sep
import time
from datetime import datetime

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .parameters import nbRecs, obs_config, paramRecs
from .tools.Convert import convertDischarge  # TODO: convertDischarge
from .tools.Criteria import calcCritClassics



class Manage():
    def __init__(self):
        self.idcompartments     = []
        self.observations       = []
        self.id_compartments    = []
        self.id_resolution      = [] 
        self.start_year         = None
        self.end_yead           = None

    class Temporal() : 
        def __init__(self) : 
            pass

        def readSimData(self, compartment, outtype, param, id_layer, syear, eyear, list_surf = [], list_point = None, tempDirectory = None, verbose = False) :
            """
            Read and convert sim data if file is MB (m3/s) to mm 

            Parameters : 
                • outfolder_path : caw output repository
                • outype : output compartment folder (ex : Output_WATBAL)
                • syear, eyear : begin and end years
                • ncells : number of cells in the resolution
                • nparams : number of recorded parameters
                • list_surface (optional) : vector of surface, need to be precise if outputs are masse balance type
                • tempDirectory : temporary file directory
            """

            stime = time.time()
            temp_file_path = tempDirectory + sep + compartment.compartment + '_' + outtype + '_' + str(syear) + str(eyear) + '_' + param +'.npy'
            if verbose: print(temp_file_path)

            if os.path.exists(temp_file_path) : 
                if verbose: print(f'Sim Matrix has already been read. Get it form .npy file : {temp_file_path}')
                simMatrix = np.load(temp_file_path)

                etime = time.time()
                if verbose: print(f'READING SIM DATA : {etime - stime} seconds')

                return simMatrix

            else :
                if verbose: print("Reading Outputs")
                outfolder_path = compartment.out_caw_path
                ncells = compartment.mesh.mesh[id_layer].ncells
                id_compartment = compartment.id_compartment
                nparams = nbRecs[compartment.compartment + '_' + outtype]

                if verbose: print(f'Output Caw directory : {outfolder_path}')
                if verbose: print(f'Numbers of cells in resolution : {ncells}')
                if verbose: print(f'Numbers of Recs parameters : {nparams}')

                # if list_surf != []: 
                #    list_surf = np.reshape(list_surf, (ncells, 1, 1))

                # binary encoding
                dtype = np.dtype([('begin', np.int32), ('values', np.float64, (ncells,)), ('end', np.int32)])

                
                # read sim data in binary file for every years
                for y in range(syear, eyear): 
                    if verbose: print(f"Period reading : {y} - {y+1}")
                    ## output file path 
                    outFileName = outfolder_path  + sep + compartment.compartment + "_" + outtype + "." + str(y) + str(y+1) + '.bin'
                    if verbose: print(outFileName)
                    ## check if the current year is bissextile and return days number
                    _ , ndays = self.check_bissextile(y+1) 
                    
                    
                    ## open binary file
                    with open(outFileName, 'rb') as file : 
                        ### read from file with numpy and reshape in a vector
                        readata = np.fromfile(file, dtype = dtype)
                        readOutNCells = readata[0][0]
                        readarray = readata['values']

                    if readOutNCells != ncells:
                        if verbose: print('WARNING : the number of cells read in the configuration is different from the number of cells in the Caw output : \n' +\
                            f'\tNumber of cells reading from configuration : {ncells}\n' + \
                                f'\tNumber of cells reading in caw output : {readOutNCells}')

                    else : 
                        if verbose: print('Year outfile has been read. Recovering data...', flush=True)

                    
                    c = 0 
                    array = []
                    for day in range(ndays):
                        array.append(readarray[c:c+nparams])
                        c += nparams

                    ## for the first iteration, init simMatrix in 3D (ncells, nparams, ndays)
                    if y == syear :
                        simMatrix = []
                        for para in range(nparams) :
                            simParam = []
                            for cell in range(ncells):
                                simParam.append([array[day][para][cell] for day in range(ndays)])
                            simMatrix.append(simParam)

                    else : 
                        for para in range(nparams) :
                            for cell in range(ncells):
                                simMatrix[para][cell] += [array[day][para][cell] for day in range(ndays)]

                    if verbose: print('Done', flush=True)
                    if verbose: print(f'Sim Matrix count {len(simMatrix[0][0])} days')
            # if verbose: print('Sim Matrix', flush=True)
            # if verbose: print(simMatrix)
                if verbose: print('Convert matrix to numpy array')
                simMatrix = np.array(simMatrix)
                if verbose: print('Done')
                for id_p, para in enumerate(paramRecs[compartment.compartment + '_' + outtype]) : 
                    temp_file_path = tempDirectory + sep + compartment.compartment + '_' + outtype + '_' + str(syear) + str(eyear) + '_' + para + '.npy'
                    if not os.path.exists(temp_file_path) : 
                        np.save(temp_file_path, simMatrix[id_p])
                        if verbose: print(f'Saved sim data in : {temp_file_path}')
                    
                return simMatrix[paramRecs[compartment.compartment + '_' + outtype].index(param)]           

        def readObsData(self, compartment, id_col_data: int, id_col_time: int, sdate: str, edate: str, verbose = False) : 
            """
            Reading observation data from .dat file 

            Parameters : 
                • compartment : compartment object
                • id_col_data : id of column containing measurements
                • id_col_time : id of column containing time vector (in caw day format)
                • sdate, edate : start and end date of simulation

            /!\ The file must not contain a column header and sep show be \s+
            """
            if verbose: print('READING OBS DATA', flush=True)
            stime = time.time()
            obs_path = compartment.obs_path # observation data path
            obs      = compartment.obs      # observation object 

            # list ids of observations points
            obs_points = [obs_id for obs_id in obs.obs_points]
            sdate = str(sdate) + '-08-01' 
            edate = str(edate) + '-07-31'

            # init mesurement dataframe which contain all observation time series
            mesurements = pd.DataFrame(index=pd.DatetimeIndex(pd.date_range(sdate, edate, freq = 'D').strftime('%Y-%m-%d').tolist()))
            
            # read record data from obs directory 
            for obs in obs_points : 
                obs_point_path = obs_path + sep + obs.id_gis + '.dat'
                if verbose: print(f'path : {obs_point_path}')

                data = pd.read_csv(
                    obs_point_path, 
                    sep = '\s+', 
                    header = None, 
                    index_col = id_col_time, 
                    parse_dates = True)
                # extract recorded data
                data = data[[id_col_data]]

                # chance index col for id od mp
                data.columns = [obs.id_gis]
                # ­data = data.loc[sdate : edate]
                # add recorded data to mesurement dataframe
                mesurements[obs.id_gis] = data[obs.id_gis]
                
            etime = time.time()
            if verbose: print(f'READING OBS DATA : {etime - stime} seconds')
            # return obs dataframe
            return mesurements

        def concatSimObs(
            self, 
            obs_point, 
            sim_matrix, 
            id_parameter : int, 
            obs_dataframe, 
            simstartyear, 
            simendyear, 
            # critsdate, 
            # critedate, 
            sdate, 
            edate, 
            post_process_directory):
            """  
            Concat obs and sim chronicle in a dataframe

            Parameters : 
                • id_obs : observation point id 
                • sim_matrix : simulated matrix 
                • id_parameter : id of simulated parameter
                • obs_dataframe : dataframe containing observations
            """
            simsdate = str(simstartyear) + '-08-01' 
            simedate = str(simendyear) + '-07-31'

            sim_data      = sim_matrix[int(obs_point.id_cell)-1]
            sim_dataframe = pd.DataFrame(sim_data, index=pd.DatetimeIndex(pd.date_range(simsdate, simedate, freq = 'D').strftime('%Y-%m-%d').tolist()))
            obs_data      = obs_dataframe[obs_point.id_gis].values
            # time_vect     = np.array(obs_dataframe.index)

            df_sim_obs = pd.concat([sim_dataframe, obs_dataframe[[obs_point.id_gis]]], axis = 1)
            df_sim_obs.columns = ['sim', 'obs']
            # df_sim_obs['sim'] = sim_data
            # df_sim_obs['obs'] = obs_data

            df_sim_obs = df_sim_obs.loc[sdate : edate]

            # Define Criteria from a SimObs DataDrame
            # df_crit = df_sim_obs.loc[critsdate : critedate]
            # crit = Crt.calcPerfStats(df_crit['sim'], df_crit['obs'])

            temp_file_path = post_process_directory + sep + sep + obs_point.id_gis + '_' + str(sdate) + '_' + str(edate) + ".dat"

            if not os.path.exists(temp_file_path):
                df_sim_obs.to_csv(temp_file_path, sep = '\t')

            else : 
                pass

            return df_sim_obs



        def readSimObs(
            self, 
            compartment, 
            outtype, 
            param,
            obs_point, 
            simstart, 
            endsim, 
            cutstart, 
            cutend, 
            id_col_data, 
            id_col_time,
            id_parameter,
            tempDirectory,
            obs_unit,
            verbose=False
            ) -> pd.DataFrame:

            simstart = str(simstart)
            endsim   = str(endsim)
            
            temp_file_path = tempDirectory + sep + str(obs_point.name) + '_' + simstart + '_' + endsim + '.npy'

            if os.path.exists(temp_file_path) : 
                if verbose: print("READING SIM OBS DATA FROM TEMP DIRECTORY")
                simobsdata = np.load(temp_file_path)

            else :
                print()
                print(obs_point, obs_point.id_layer, obs_point.id_cell)
                print(compartment)

                if verbose: print("SIMOBS CHRONICLE DOESN'T EXISTS IN TEMP DIRECTORY. READ IT FROM SIM OUTPUT AND OBS DATA")
                simdata = self.readSimData(
                    compartment = compartment, 
                    outtype = outtype, 
                    param = param,
                    id_layer = obs_point.id_layer,
                    syear = int(simstart), 
                    eyear = int(endsim), 
                    tempDirectory = tempDirectory
                )

                print(simdata.shape)  # readSimData reads wrong matrix (mesh from layer 0) despite layer 1 being selected
                
                
                obsdata= self.readObsData(
                    compartment = compartment, 
                    id_col_data = id_col_data,
                    id_col_time= id_col_time, 
                    sdate = simstart, 
                    edate=endsim
                )

                simobsdata = self.concatSimObs(
                    obs_point = obs_point, 
                    sim_matrix=simdata, 
                    id_parameter=id_parameter, 
                    obs_dataframe=obsdata, 
                    simstartyear=simstart, 
                    simendyear=endsim,
                    sdate = cutstart, 
                    edate = cutend, 
                    post_process_directory=tempDirectory
                )

                if compartment.compartment == 'HYD' :
                    simobsdata['obs'] = convertDischarge(simobsdata['obs'], obs_unit)

            return simobsdata

        def plotSimObs(self, compartment, outtype, param, simstartyear, simendyear, plotstartdate, plotenddate, id_layer, obs_point, id_parameter, post_process_directory, ylabel, obs_unit, verbose = False) : 
            """
            Plot Sim and Obs variable in a matplotlib graph object

            Parameters : 
                compartment :
                resolutionName :
                outtype : 
                simstartyear, simendyear : start and end dates of the simulated period
                plotstartyear, plotendyear : start and end dates of the plotted period
                id_layer :
                obs_point :
                id_parameter : 
                post_process_directory : 
                ylabel :

            """

            # Check whether sim and obs files have already been read
            temp_file_path = post_process_directory + sep + "TEMP" + str(obs_point.id_gis) + ".dat"
            

            if os.path.exists(temp_file_path):
                df_sim_obs = pd.read(temp_file_path)

            else :
                id_col_time = obs_config[compartment.id_compartment]['id_col_time']
                id_col_data = obs_config[compartment.id_compartment]['id_col_data']
                sim_matrix  = self.readSimData(compartment, outtype, param, id_layer, simstartyear, simendyear,  tempDirectory=post_process_directory + sep + 'TEMP')
                obs_df      = self.readObsData(compartment, id_col_data, id_col_time, plotstartdate, plotenddate)
                df_sim_obs  = self.concatSimObs(obs_point, sim_matrix, id_parameter, obs_df, simstartyear, simendyear, plotstartdate, plotenddate, post_process_directory)
                
                if compartment.compartment == 'HYD' :
                    df_sim_obs['obs'] = convertDischarge(df_sim_obs['obs'], obs_unit)

                elif compartment.compartment == 'AQ' :
                    pass

                else : 
                    pass

            # df_sim_obs['obs'] = df_sim_obs['obs']
            if verbose: print(f'obs id : {obs_point.id_gis}')
            # if verbose: print(df_sim_obs)
            df_sim_obs.index = pd.to_datetime(df_sim_obs.index)

            fig, ax = plt.subplots()

            # df = df_sim_obs.loc[sdate : edate]

            # Plot obs values 
            df_sim_obs['obs'].plot(ax = ax, color = 'green', marker = 'o', linestyle = '', legend = 'Observed', markersize = 0.8)

            # Plot sim values
            df_sim_obs['sim'].plot(ax = ax, color = 'red', legend = 'Simulated', linewidth = 0.5)

            

            crit = calcCritClassics(df_sim_obs['sim'].values, df_sim_obs['obs'].values)
            # Set graph title 
            title = f'{obs_point.name} - {obs_point.id_gis} (id caw cell : {obs_point.id_cell}) \n' + \
                str([f'{key} : {round(value, 2)} ' for key, value in crit.items()])
            ax.set_title(title)
            ax.set_ylabel(ylabel)

            return fig

        def plotPDF(self, compartment, outtype, param, simsdate, simedate, plotstartdate, plotenddate, id_layer, obs_points, id_parameter, outPP, name_file, ylabel, obs_unit, verbose=False):
            stime = time.time()
            pdf_file_path = outPP + sep + name_file + '.pdf'
            with PdfPages(pdf_file_path) as pdf : 
                for obs in obs_points : 
                    #if verbose: print(obs.name)
                    fig = self.plotSimObs(compartment, outtype, param, simsdate, simedate, plotstartdate, plotenddate, id_layer, obs, id_parameter, outPP, ylabel, obs_unit)
                    # fig.show()
                    pdf.savefig(fig, orientation = 'portrait')
                    #plt.close(fig)

                #if verbose: print(f'Done : save → {outPP + sep + name_file + ".pdf"}')

            etime = time.time()
            if verbose: print(f'READING PLOT PDF : {etime - stime} seconds')
                
        def interactifplotSimObs(self, df_sim_obs, id_point) : 
            pass

        def check_bissextile(self, year) : 
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) :
                return (True, 366)
            else : 
                return (False, 365)

        def convertDatestoCawDay(days : list, startsim = '1970-08-01') : 
            start_caw_day = datetime.strptime(startsim, "%Y-%m-%d")

            caw_format_dates = []

            for day_str in days :
                day      = datetime.strptime(day_str, "%Y-%m-%d")
                day_diff = day - start_caw_day

                caw_format_dates.append(day_diff.days + 1)

            return caw_format_dates 
        
        def simMatrixToDf(self, matrix, syear, eyear, cutsdate = None, cutedate = None) : 
            dates = pd.date_range(start=f'{syear}-08-01', end=f'{eyear}-07-31')
            df_sim = pd.DataFrame(matrix.T, index = dates)

            if cutedate != None and cutsdate != None : 
                df_sim = df_sim.loc[f'{syear}-08-01' : f'{eyear}-07-31']

            return df_sim
            

        def aggregate_matrix(self, df, agg_dimension, syear, eyear) :
            """
            Aggragate given matrix according specified aggragator on a specied matrix 
            dimension 

            Paremeters : 
                • df : time series wanted to be aggragate (meshes, recorded parameter, nday)
                • aggragator : mean or interanual
                • agg_dimention : set 1 to agregate on time
                • syear, eyear : begin and final year
            """
            
            if agg_dimension == 'interanual':
                return df.resample('A-AUG').sum().mean().to_list()
            
            if agg_dimension == 'daily' : 
                return df.mean().to_list()

            # if aggregator == 'daily' : 
            #     return np.mean(matrix, agg_dimension).reshape(-1)

            # if aggregator == 'interanual' : 
            #     return np.reshape(np.sum(matrix, agg_dimension) / (eyear - syear), -1)
            

        def plot_spatialmap(simMatrix, mesh) : 
            pass


    class Budget() : 
        def __init__() : 
            raise NotImplementedError()

    class Spatial() : 
        def __init__(self) : 
            raise NotImplementedError()
