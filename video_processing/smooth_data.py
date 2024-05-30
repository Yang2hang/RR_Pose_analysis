import numpy as np
import pandas as pd
from scipy.interpolate import make_smoothing_spline

def smooth_data(df, columns, logger):
    """
    Identify qualified trials (start with y > 90 and entered T-entry (y < 46))
    Smooths the data from the warped df by identifying trials
    and applying a smoothing spline to each trial segment.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the data to be smoothed.
                           It is assumed to have 'warped Head x' and 'warped Head y' columns.
    columns: A list of columns in df to be smoothed
    
    Returns:
    pandas.DataFrame: A new smoothed DataFrame containing only the rows that meet the trial requirements.
    """
    trial_num = 0
    record_trial = False
    T_entry = False
    start_index = 0
    smoothed_data_list = []
    valid_rows = []
    elapsed_times = []
    total_frames = len(df)
    
    for index, row in df.iterrows():
        y = row['warped Head y']

        if not record_trial:
            if y > 90:  # 0>_000_0 First frame of one trial
                # Reset all flags
                record_trial = True
                T_entry = False
                trial_num += 1
                start_index = index
                elapsed_times = []

        if record_trial:  # in a trial
            elapsed_time = (index - start_index) * 1 / 30 
            elapsed_times.append(elapsed_time)

            if not T_entry and y < 46:  # Enter T-junction
                T_entry = True
            if T_entry and y > 50:  # 0_000_>0 (last + 1) frame of each trial
                smoothing_data = {}
                trial_len = len(range(start_index, index))
                grid = np.linspace(1, trial_len, trial_len)

                for column in columns:
                    smoothing_column = df[start_index:index][column]
                    spline = make_smoothing_spline(grid, smoothing_column)
                    smoothing_data[column] = spline(grid)
                smoothed_section = pd.DataFrame(smoothing_data)
                smoothed_section['Elapsed Time'] = elapsed_times[:trial_len]
                smoothed_data_list.append(smoothed_section)

                # Add the valid rows to the list
                valid_rows.extend(range(start_index, index))

                # Reset all flags
                record_trial = False
                T_entry = False
                
                if y > 90:  # 0_000_>_ First frame of next trial
                    # Set all flags
                    record_trial = True
                    T_entry = False
                    trial_num += 1
                    start_index = index
                    elapsed_times = []
                    elapsed_time = (index - start_index) * 1 / 30 
                    elapsed_times.append(elapsed_time)

    if record_trial:  # Deal with the last trial if still recording
        smoothing_data = {}
        trial_len = len(range(start_index, index + 1))
        grid = np.linspace(1, trial_len, trial_len)
        for column in columns:
            smoothing_column = df[start_index:index + 1][column]
            spline = make_smoothing_spline(grid, smoothing_column)
            smoothing_data[column] = spline(grid)
        
        smoothed_section = pd.DataFrame(smoothing_data)
        smoothed_section['Elapsed Time'] = elapsed_times
        smoothed_data_list.append(smoothed_section)

        # Add the valid rows to the list
        valid_rows.extend(range(start_index, index + 1))

    smoothed_data = pd.concat(smoothed_data_list).reset_index(drop=True)

    # Create a DataFrame containing only the valid rows from the original DataFrame
    valid_df = df.iloc[valid_rows].reset_index(drop=True)

    # Ensure the smoothed data and valid data have the same indices
    valid_df[columns] = smoothed_data[columns]
    valid_df['Elapsed Time'] = smoothed_data['Elapsed Time']
    
    # Calculate and log discard frames number and discard rate
    discarded_frames = total_frames - len(valid_df)
    discard_rate = discarded_frames / total_frames
    logger.info(f"DataFrame processed. Discarded frames: {discarded_frames}, Discard rate: {discard_rate:.2%}")

    return valid_df
