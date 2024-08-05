import numpy as np
import pandas as pd

def get_trial_profile(df, speed_threshold=500, speed_length=12, coord_length=13):
    """
    Extracts the straight walking speed curve, trajectory, average speed, and final decision for each trial.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the labeled data with decisions.
    speed_threshold (float): The threshold above which speeds are considered outliers and are filtered out.
    length_threshold (int): The target length for normalization of speed profiles. Profiles shorter than this are excluded.
    coord_length (int): The number of coordinate points to extract before each decision.
    
    Returns:
    pandas.DataFrame: A DataFrame with each row representing a trial, containing columns
                      for the trial number, speed profile, coordinate data, and the final decision.
    """
    current_trial_num = np.nan
    current_decision = np.nan
    decision = np.nan
    
    trials = []
    current_trial_speeds = []
    current_trial_coords = []

    for index, row in df.iterrows():
        trial_num = row['trial']
        decision = row['decision']
        speed = np.sqrt(row['Head_vx']**2 + row['Head_vy']**2)

        head_x = row['warped Head x']
        head_y = row['warped Head y']
        
        if not pd.isna(decision): # Decision != None, update current decision
            current_decision = decision    
            
        if trial_num != current_trial_num: # Start of a new trial
            
            if len(current_trial_speeds) >= speed_length and len(current_trial_coords) >= coord_length * 2:
                # Use the last `speed_length` frames of speed values and `coord_length` frames of coordinates as the profile
                normalized_speeds = current_trial_speeds[-speed_length:]
                normalized_coords = current_trial_coords[-(coord_length * 2):]
                x1, y1 = normalized_coords[0], normalized_coords[1]
                x2, y2 = normalized_coords[-2], normalized_coords[-1]
                distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                average_speed = distance / ((coord_length - 1) / 30)
                trials.append([normalized_speeds, normalized_coords, current_decision, average_speed])
                
            current_trial_speeds = []
            current_trial_coords = []
            current_decision = np.nan
            current_trial_num = trial_num

        if pd.isna(current_decision) and index != 0: # Straight walking speed
            if speed < speed_threshold:
                current_trial_speeds.append(speed)
                current_trial_coords.append(head_x)
                current_trial_coords.append(head_y)
        
    # Handle the final trial
    if not pd.isna(current_decision) and len(current_trial_speeds) >= speed_length and len(current_trial_coords) >= coord_length * 2:
        normalized_speeds = current_trial_speeds[-speed_length:]
        normalized_coords = current_trial_coords[-(coord_length * 2):]
        x1, y1 = normalized_coords[0], normalized_coords[1]
        x2, y2 = normalized_coords[-2], normalized_coords[-1]
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        average_speed = distance / ((coord_length - 1) / 30)
        trials.append([normalized_speeds, normalized_coords, current_decision, average_speed])
    
    # Convert the list of trials to a DataFrame with appropriate column names
    speed_profiles = [t[0] for t in trials]
    coord_profiles = [t[1] for t in trials]
    decisions = [t[2] for t in trials]
    average_speeds = [t[3] for t in trials]

    # Flatten coordinate profiles into individual columns
    coord_columns = [f'x{i//2+1}' if i % 2 == 0 else f'y{i//2+1}' for i in range(coord_length * 2)]
    
    profiles_df = pd.DataFrame(speed_profiles, columns=[f'speed {i+1}' for i in range(speed_length)])
    coords_df = pd.DataFrame(coord_profiles, columns=coord_columns)
    
    profiles_df['final decision'] = decisions
    profiles_df['average speed'] = average_speeds
    final_df = pd.concat([profiles_df, coords_df], axis=1)

    return final_df