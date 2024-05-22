import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

def get_displacement(df, bodyparts):
    """
    Calculate the displacement for the specified body parts and add them to the DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate displacements for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).

    Returns:
    pandas.DataFrame: A new DataFrame with displacement columns added.
    """
    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        x_col = f"warped {bodypart} x"
        y_col = f"warped {bodypart} y"
        displacement_col = f"{bodypart}_displacement"
        displacements = [0]  # Initial displacement is 0

        for i in range(1, len(df)):
            xd = df[x_col].iloc[i] - df[x_col].iloc[i - 1]
            yd = df[y_col].iloc[i] - df[y_col].iloc[i - 1]
            displacements.append(np.sqrt(xd ** 2 + yd ** 2))

        df[displacement_col] = displacements
    return df

def get_velocity(df, bodyparts, frame_rate, sigma=3):
    """
    Calculate the velocity for the specified body parts and add them to the DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate velocities for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).
    frame_rate (float): Frame rate of the video.
    sigma (int): Standard deviation for Gaussian kernel.

    Returns:
    pandas.DataFrame: A new DataFrame with velocity columns added.
    """
    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        displacement_col = f"{bodypart}_displacement"
        velocity_col = f"{bodypart}_velocity"
        raw_velocity = df[displacement_col] / (1 / frame_rate)
        filtered_velocity = gaussian_filter1d(raw_velocity, sigma)
        df[velocity_col] = filtered_velocity
    return df

def get_acceleration(df, bodyparts, frame_rate):
    """
    Calculate the acceleration for the specified body parts and add them to the DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the coordinates.
    bodyparts (str or list): A body part or list of body parts to calculate accelerations for (e.g., 'Head' or ['Head', 'Torso', 'Tailhead']).
    frame_rate (float): Frame rate of the video.

    Returns:
    pandas.DataFrame: A new DataFrame with acceleration columns added.
    """
    if isinstance(bodyparts, str):
        bodyparts = [bodyparts]

    for bodypart in bodyparts:
        velocity_col = f"{bodypart}_velocity"
        acceleration_col = f"{bodypart}_acceleration"
        node_velocity = df[velocity_col]
        nextframe = np.append(np.delete(node_velocity.values, 0), node_velocity.values[-1])
        acceleration = (nextframe - node_velocity) / (1 / frame_rate)
        df[acceleration_col] = acceleration
    return df
