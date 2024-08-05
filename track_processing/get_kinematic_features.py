import numpy as np
from scipy import stats

def get_kinematic_features(trial_df, sr=30):
    """
    Calculate the angular velocities based on neck-head orientation and head velocity changes.
    
    Parameters:
    trial_df (pd.DataFrame): DataFrame containing the time series data with columns for Neck x, Neck y, Head x, and Head y.
    sr (float): Sampling rate.
    
    Returns:
    pd.DataFrame: DataFrame with calculated angular velocities and their sum.
    """
    # Calculate the neck-head orientation angles
    neck_head_angles = np.arctan2(trial_df['warped Head y'] - trial_df['warped Neck y'], trial_df['warped Head x'] - trial_df['warped Neck x'])
    neck_head_angles_unwrapped = np.unwrap(neck_head_angles)
    angular_velocity = np.gradient(neck_head_angles_unwrapped) * sr
    
    # Calculate the head velocity
    head_velocity_x = np.gradient(trial_df['warped Head x']) * sr
    head_velocity_y = np.gradient(trial_df['warped Head y']) * sr
    head_speed = np.sqrt(head_velocity_x**2 + head_velocity_y**2)
    
    # Calculate VTE
    dx = np.gradient(trial_df['warped Head x'])
    dy = np.gradient(trial_df['warped Head y'])
    Phi = np.unwrap(np.arctan2(dy, dx))
    dPhi = np.abs(np.gradient(Phi))
    
    # Calculate the head velocity angles
    # head_velocity_angles = np.arctan2(head_velocity_y, head_velocity_x)
    # head_velocity_angles_unwrapped = np.unwrap(head_velocity_angles)
    # revolution = np.gradient(head_velocity_angles_unwrapped) * sr
    
    # Calculate the sum of the two angular velocities
    
    trial_df['Head_vx'] = head_velocity_x
    trial_df['Head_vy'] = head_velocity_y
    trial_df['Head_v'] = head_speed
    trial_df['angular_velocity'] = angular_velocity
    trial_df['dPhi'] = dPhi
    
    return trial_df