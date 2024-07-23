import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

def get_displacement(raw_df, bodyparts):
    """
    TODO np.gradient, add a speed (scalar) column
    Calculate the displacement for the specified body parts and add them to the DataFrame.

    Parameters:
    raw_df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate displacements for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).

    Returns:
    pandas.DataFrame: A new DataFrame with displacement columns added.
    """
    df = raw_df.copy()
    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        x_col = f"warped {bodypart} x"
        y_col = f"warped {bodypart} y"
        disp_x_col = f"{bodypart} displacement x"
        disp_y_col = f"{bodypart} displacement y"
        
        df[disp_x_col] = 0
        df[disp_y_col] = 0
        
        for trial_number, group in df.groupby('trial'):
            displacements_x = [0]  # Initial displacement x is 0 for the first frame of each trial
            displacements_y = [0]  # Initial displacement y is 0 for the first frame of each trial
            
            for i in range(1, len(group)):
                xd = group[x_col].iloc[i] - group[x_col].iloc[i - 1]
                yd = group[y_col].iloc[i] - group[y_col].iloc[i - 1]
                displacements_x.append(xd)
                displacements_y.append(yd)
            
            df.loc[group.index, disp_x_col] = displacements_x
            df.loc[group.index, disp_y_col] = displacements_y
    
    return df

def get_velocity(raw_df, bodyparts, sr):
    """
    Calculate the velocity for the specified body parts and add them to the DataFrame.
    Make sure the coordinates are equidistant.

    Parameters:
    raw_df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate velocities for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).
    frame_rate (float): Frame rate of the video.

    Returns:
    pandas.DataFrame: A new DataFrame with velocity columns added.
    """
    df = raw_df.copy()
    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        disp_x_col = f"{bodypart} displacement x"
        disp_y_col = f"{bodypart} displacement y"
        vel_x_col = f"{bodypart} velocity x"
        vel_y_col = f"{bodypart} velocity y"
        speed_col = f'{bodypart} speed'
        
        df[vel_x_col] = 0
        df[vel_y_col] = 0
        
        for trial_number, group in df.groupby('trial'):
            velocities_x = [0]  # Initial velocity x is 0 for the first frame of each trial
            velocities_y = [0]  # Initial velocity y is 0 for the first frame of each trial
            
            for i in range(1, len(group)):
                vx = group[disp_x_col].iloc[i] / (1 / sr)
                vy = group[disp_y_col].iloc[i] / (1 / sr)
                velocities_x.append(vx)
                velocities_y.append(vy)
            
            df.loc[group.index, vel_x_col] = velocities_x
            df.loc[group.index, vel_y_col] = velocities_y
    
    return df

def get_acceleration(raw_df, bodyparts, sr):
    """
    Calculate the acceleration for the specified body parts and add them to the DataFrame.

    Parameters:
    raw_df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate accelerations for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).
    frame_rate (float): Frame rate of the video.

    Returns:
    pandas.DataFrame: A new DataFrame with acceleration columns added.
    """
    df = raw_df.copy()

    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        vel_x_col = f"{bodypart} velocity x"
        vel_y_col = f"{bodypart} velocity y"
        acc_x_col = f"{bodypart} acceleration x"
        acc_y_col = f"{bodypart} acceleration y"
        
        df[acc_x_col] = 0
        df[acc_y_col] = 0
        
        for trial_number, group in df.groupby('trial'):
            accelerations_x = [0, 0]  # Initial accelerations x are 0 for the first two frames of each trial
            accelerations_y = [0, 0]  # Initial accelerations y are 0 for the first two frames of each trial
            
            for i in range(2, len(group)):
                ax = (group[vel_x_col].iloc[i] - group[vel_x_col].iloc[i - 1]) / (1 / sr)
                ay = (group[vel_y_col].iloc[i] - group[vel_y_col].iloc[i - 1]) / (1 / sr)
                accelerations_x.append(ax)
                accelerations_y.append(ay)
            
            df.loc[group.index, acc_x_col] = accelerations_x
            df.loc[group.index, acc_y_col] = accelerations_y
    
    return df
