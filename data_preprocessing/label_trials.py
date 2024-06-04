import pandas as pd

def label_trials(df, filename):
    """
    Labels the trial number for each row based on the criteria:
    - y > 90 as the beginning of a trial
    - y < 46 as T-entry
    - T-entry and y > 90 as the start of the next trial

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing 'warped Head y' column.

    Returns:
    pandas.DataFrame: A DataFrame with an additional column 'trial num' that labels each row with the trial number.
    """
    T_entry = False
    camera_num = int(filename.split('_')[2][1])
    trial_num = camera_num
    
    trial_labels = []
    
    for index, row in df.iterrows():
        y = row['warped Head y']
        
        if T_entry and y > 90:  # Start of a new trial
            trial_num += 4
            T_entry = False
        
        elif not T_entry and y < 46:  # Enter T-junction
            T_entry = True            
        
        # Assign the current trial number to the row
        trial_labels.append(trial_num)

    # Add the trial number labels to the DataFrame
    df['trial num'] = trial_labels

    return df
