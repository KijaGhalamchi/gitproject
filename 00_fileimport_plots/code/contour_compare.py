import numpy as np
import matplotlib.pyplot as plt
import csv_import
import os

### 2D Contour plots for different x/D positions and variables to compare ###
### Use only for unstructured grids, since tricontour is specified for unstructured grids. ###

# Input: List with variables to plot, given as strings
# Available variables: 'T', 'p', 'rho', 'CH4', 'CO2', 'N2', 'O2', 'CO', 'OH', 'H2O', 'H2'
def ncontours(variables):
    #amount of columns for subplots and the corresponding labels:
    col = 0
    labels_xD = []
    #amount of rows for each variable which we want to plot
    rows = len(variables)

    #Define current path (IDLE!)
    path = os.getcwd()

    #Get .csv files from dir
    for entry in os.scandir(path):
        if(entry.name.endswith('.csv')):
            col = col+1
            plotname = entry.name.split(".")[0]
            labels_xD.append(plotname)

    fig, axis = plt.subplots(nrows=rows, ncols=col, sharex=True, sharey=True, constrained_layout=True, figsize=(8 + 8*(col-1), 8 + 8*(rows-1)))

    #Figure title
    figtitle = 'Contourplots of variables '
    for i, item in enumerate(variables):
        if i:
            figtitle = figtitle + ', '
        figtitle = figtitle + item



    # axis data
    #y = csv_import.csvimport('xD120.csv')["y"]
    #z = csv_import.csvimport('xD120.csv')["z"]

    #subplots
    for i in range(rows):
        var = variables[i]
        #Getting variable unit for colorbar
        if var == 'T':
            unit = '[K]'
        elif var == 'p':
            unit = '[Pa]'
        elif var == 'rho':
            unit = '[kg/m³]'
        else: unit = 'Y'


        for j in range(col):
            #y and z point values differ for each x/D due to the unstructured grid
            y = csv_import.csvimport(labels_xD[j]+'.csv')["y"]
            z = csv_import.csvimport(labels_xD[j]+'.csv')["z"]
            #Getting raw values
            varvalues = csv_import.csvimport(labels_xD[j]+'.csv')[var]
            var_max = varvalues.max()
            var_min = varvalues.min()
            ### NORMALIZATION ###
            varvalues_N = np.empty(shape=varvalues.shape)
            for t in range(len(varvalues)):
                varvalues_N[t] = (varvalues[t] - var_min)/(var_max-var_min)
            #####################
            ###If only one variable available (different array dimension)
            if(rows==1):
                ### NORMALIZED LEVELS
                levels = np.linspace(0, 1, 100)
                ### LEVELS OF RAW VALUES ###
                # levels = np.linspace(var_min, var_max, 100)
                temp = axis[j].tricontourf(y, z, varvalues_N, levels=levels, cmap='jet')
                ### RAW VALUES - NOT NORMALIZED ###
                # temp = axis[j].tricontourf(y, z, varvalues, levels=levels, cmap='jet')

                # axis labels
                axis[j].set_xlabel('y', fontsize=15, labelpad=-3)
                axis[j].set_ylabel('z', fontsize=15, labelpad=2)
                axis[j].title.set_text(var + ' at ' + 'x/D = ' + labels_xD[j].split("D")[1])

                # colorbar
                # if Normalized -> No cbar title.
                plt.colorbar(temp, ax=axis[j])
                # cbar = plt.colorbar(temp, ax=axis[j])
                # cbar.ax.set_title(unit, fontsize=20)

            else: #More than one variable (ndimensional array)
                ### NORMALIZED LEVELS
                levels = np.linspace(0, 1, 100)
                ### LEVELS OF RAW VALUES ###
                #levels = np.linspace(var_min, var_max, 100)
                temp = axis[i,j].tricontourf(y, z, varvalues_N, levels=levels, cmap='jet')
                ### RAW VALUES - NOT NORMALIZED ###
                #temp = axis[i, j].tricontourf(y, z, varvalues, levels=levels, cmap='jet')

                #axis labels
                axis[i,j].set_xlabel('y', fontsize=15, labelpad=3)
                axis[i,j].set_ylabel('z', fontsize=15, labelpad=2)
                axis[i,j].title.set_text(var + ' at ' + 'x/D = ' + labels_xD[j].split("D")[1])

                #colorbar
                # if Normalized -> No cbar title.
                plt.colorbar(temp, ax=axis[i,j])
                #cbar = plt.colorbar(temp, ax=axis[i, j])
                #cbar.ax.set_title(unit, fontsize=20)

                #Set Limits for zoom
    plt.xlim([-0.025, 0.025])
    plt.ylim([-0.025, 0.025])

    plt.show()
    return

ncontours(['CO', 'CO2'])
