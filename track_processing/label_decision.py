import numpy as np
import pandas as pd
import cv2

def get_decision_thresholds(filename, logger):
    try:
        if 'R1' in str(filename):
            srcTri = np.array([[186.9, 178.3], [226, 178.3], [224, 137.6]]).astype(np.float32)
        elif 'R2' in str(filename):
            srcTri = np.array([[271.2, 128.3], [270.8, 95.6], [228.7, 95.3]]).astype(np.float32)
        elif 'R3' in str(filename):
            srcTri = np.array([[208.5, 53.5], [170, 54.5], [170.7, 89.5]]).astype(np.float32)
        elif 'R4' in str(filename):
            srcTri = np.array([[108.4, 119.3], [109.1, 158.5], [155.3, 159.2]]).astype(np.float32)
        else:
            logger.error(f"Cannot find warp matrix for this file: {filename}")
            return None

        dstTri = np.array([[350, 46], [350, 10], [309, 10]]).astype(np.float32)
        warp_matrix = cv2.getAffineTransform(srcTri, dstTri)
        return warp_matrix
    except Exception as e:
        logger.error(f"Error calculating warp matrix for {filename}: {e}")
        raise
    
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
                decision = 'T-Entry'

        if decision == 'T-Entry':
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
