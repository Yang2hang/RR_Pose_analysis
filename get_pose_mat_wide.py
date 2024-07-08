import numpy as np
import pandas as pd

def get_pose_mat_wide(pose_mat_long, frames_preserved):
    '''
    Transpose the long pose mat into a wide one and calculate relevant features along the way.

    Parameters:
    pose_mat_long (pd.DataFrame): The long form DataFrame containing pose data.
    frames_preserved (int): The number of frames to preserve for each trial.

    Returns:
    result_df (pd.DataFrame): The wide form DataFrame with preserved frames and trial-wise features.
    '''
    current_trial_num = np.nan
    current_sleap_decision = np.nan
    current_bonsai_decision = np.nan
    sleap_decision = np.nan
    bonsai_decision = np.nan
    current_length = 0
    sum_of_speed = 0
    speed_count = 0

    sleap_decision_list = []
    bonsai_decision_list = []
    straight_walking_speed_list = []
    animal_list = []
    session_list = []
    trial_list = []
    restaurant_list = []
    trial_lengths = []
    current_trial_coords = []
    preserved_coords = []

    for index, row in pose_mat_long.iterrows():
        trial_num = row['trial']

        if not np.isnan(current_trial_num) and (trial_num != current_trial_num):  # Start of a new trial
            if speed_count != 0:
                average_speed = sum_of_speed / speed_count
            else:
                average_speed = np.nan

            if len(current_trial_coords) >= frames_preserved * 2:
                preserved_coords.append(current_trial_coords[:(frames_preserved * 2)])
                sleap_decision_list.append(current_sleap_decision)
                bonsai_decision_list.append(current_bonsai_decision)
                straight_walking_speed_list.append(average_speed)
                animal_list.append(animal)
                session_list.append(session)
                trial_list.append(current_trial_num)
                restaurant_list.append(restaurant)
                trial_lengths.append(current_length)

            animal = row['animal']
            session = row['session']
            speed = np.sqrt(row['Head velocity x']**2 + row['Head velocity y']**2)
            restaurant = row['restaurant']
            head_x = row['warped Head x']
            head_y = row['warped Head y']
            sleap_decision = row['decision']
            bonsai_decision = row['label']
            
            current_sleap_decision = np.nan
            current_bonsai_decision = np.nan
            current_trial_num = trial_num
            sum_of_speed = 0
            speed_count = 0
            current_length = 1
            current_trial_coords = [head_x, head_y]
            
        else:  # Within trial
            animal = row['animal']
            session = row['session']
            speed = np.sqrt(row['Head velocity x']**2 + row['Head velocity y']**2)
            restaurant = row['restaurant']
            head_x = row['warped Head x']
            head_y = row['warped Head y']
            sleap_decision = row['decision']
            bonsai_decision = row['label']
            
            current_length += 1
            current_trial_coords.append(head_x)
            current_trial_coords.append(head_y)
            
            current_trial_num = trial_num

        if not pd.isna(sleap_decision):  # update current_sleap_decision
            current_sleap_decision = sleap_decision
        if not pd.isna(bonsai_decision): # update current_consai_decision
            current_bonsai_decision = bonsai_decision
            
        if pd.isna(current_sleap_decision) and (speed < 300) and (speed != 0):  # calculate straight walking speed and discard outliers
            sum_of_speed += speed
            speed_count += 1

    coord_columns = [f'x{i // 2 + 1}' if i % 2 == 0 else f'y{i // 2 + 1}' for i in range(frames_preserved * 2)]
    coords_df = pd.DataFrame(preserved_coords, columns=coord_columns)

    other_df = pd.DataFrame({
        'sleap_decision': sleap_decision_list,
        'bonsai_decision': bonsai_decision_list,
        'straight_walking_speed': straight_walking_speed_list,
        'animal': animal_list,
        'session': session_list,
        'trial': trial_list,
        'restaurant': restaurant_list,
        'trial_length': trial_lengths,
    })

    result_df = pd.concat([coords_df, other_df], axis=1)
    return result_df