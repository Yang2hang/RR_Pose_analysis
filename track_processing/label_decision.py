import numpy as np
import pandas as pd
import cv2
    
def label_decision(df, filename, logger):
    """
    TODO should use groupby and apply function
    Updates the DataFrame in real time, adding a new column with the current state
    (T-entry, Acc, Rej, quit) for each timepoint.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the smoothed data.
                           It is assumed to have 'warped Head x' and 'warped Head y' columns.

    Returns:
    pandas.DataFrame: A DataFrame with the decision for each timepoint.
    """
    current_trial = None
    decisions = []
    decision = None
    last_decision = None
    
    try:
        if 'R1' in str(filename):
            t_entry_threshold = 48
            rej_threshold = 278
            acc_threshold = 314
        elif 'R2' in str(filename):
            t_entry_threshold = 44
            rej_threshold = 279
            acc_threshold = 308
        elif 'R3' in str(filename):
            t_entry_threshold = 49
            rej_threshold = 279
            acc_threshold = 306
        elif 'R4' in str(filename):
            t_entry_threshold = 50
            rej_threshold = 276
            acc_threshold = 311
        else:
            logger.error(f"Cannot find decision thresholds for this file: {filename}")
    except Exception as e:
        logger.error(f"Error calculating warp matrix for {filename}: {e}")
        raise
    
    for index, row in df.iterrows():
        x = row['warped Head x']
        y = row['warped Head y']
        trial = row['trial']
        
        if current_trial != trial: # 0>_000_0 Start of a new trial
            decision = None
            last_decision = None
            current_trial = trial

        if (decision == None):
            if y < t_entry_threshold: # entering T-entry
                decision = 'T_Entry'

        if decision == 'T_Entry':
            if x > acc_threshold:
                decision = 'ACC'
            elif x < rej_threshold:
                decision = 'REJ'

        if decision == 'ACC':
            if x < rej_threshold:
                decision = 'quit'

        # Only append the decision if it has changed, otherwise append None
        if decision != last_decision:
            decisions.append(decision)
            last_decision = decision
        else:
            decisions.append(None)     
    
    # Add the decisions column to the DataFrame
    df['decision'] = decisions

    return df
