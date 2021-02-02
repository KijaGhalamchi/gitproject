import pandas as pd
import numpy as np
import pathlib
import glob

def read_lines(path):
    """
    Reads the probes (lines) located in the path directory.
    The data is stored in a pd.Dataframe with an additional entry for the time-step.
    """
    files = sorted(glob.glob(path))
    df = pd.DataFrame()
    for file in files:
        path = pathlib.PurePath(file)
        # Extract the time (folder name)
        time = float(path.parent.name)

        # Extract the variable names (seperated by _)
        fileName = path.name
        fileName = fileName[:-3]
        headers = fileName.split('_')
        headers[0] = 'x'
        if 'U' in headers:
            idx = headers.index('U')
            headers[idx] = 'Uz'
            headers.insert(idx, 'Uy')
            headers.insert(idx, 'Ux')

        # Read in data and store in df
        data = np.genfromtxt(file)
        tmp=pd.DataFrame(data,columns=headers)
        tmp['t'] = time
        df = df.append(tmp, ignore_index=True)
        
    df.sort_values(['t','x'], inplace=True)
    print("  Finished reading {} timesteps.".format(len(df['t'].unique())))
    print("    min(t)={}, max(t)={}.".format(np.min(df['t']), np.max(df['t'])))
    return df

def read_surface(path):
    """
    Reads the probes (lines) located in the path directory.
    The data is stored in a pd.Dataframe with an additional entry for the time-step.
    """
    files = sorted(glob.glob(path))
    df = pd.DataFrame()
    print(files)
    # Set the grid:
    headers = ['x', 'y', 'z']
    # Read in data and store in df
    data = np.genfromtxt(files[0])
    tmp=pd.DataFrame(data[...,:3],columns=headers)
    print(tmp)
    for file in files:
        path = pathlib.PurePath(file)
        fileName = path.name
        print(fileName)
        var = fileName.split('_')[0]
        
        # Read in data and store in df
        data = np.genfromtxt(file)
        tmp[var] = data[..., -1]
    return tmp
read_surface('xD_12data0.csv')

