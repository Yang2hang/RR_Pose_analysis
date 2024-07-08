import numpy as np
import pandas as pd
from scipy.interpolate import make_smoothing_spline

def smooth_data(df, columns, logger):
    """
    Identify each trial.
    Smooths the trial-wise data by applying a smoothing spline to each trial segment.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data to be smoothed.
                           It is assumed to have 'warped Head x' and 'warped Head y' columns.
    columns: A list of columns in df to be smoothed
    
    Returns:
    pandas.DataFrame: A new smoothed DataFrame containing only the rows that meet the trial requirements.
    """
    smoothed_dfs = []
    
    for trial_number, group in df.groupby('trial'):
        trial_len = len(group)
        grid = np.linspace(1, trial_len, trial_len)
        
        for column in columns:
            smoothing_column = group[column].values
            spline = make_smoothing_spline(grid, smoothing_column)
            group.loc[:, column] = spline(grid)  # Update the smoothed column in place
        
        smoothed_dfs.append(group)

    # Concatenate all smoothed sections
    smoothed_df = pd.concat(smoothed_dfs, axis=0, ignore_index=True).reset_index(drop=True)

    return smoothed_df