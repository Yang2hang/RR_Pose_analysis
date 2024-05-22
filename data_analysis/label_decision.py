import numpy as np
import pandas as pd

def label_decision(df):
    """
    Updates the DataFrame in real time, adding a new column with the current state
    (T-entry, Acc, Rej, quit) for each timepoint.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the smoothed data.
                           It is assumed to have 'warped Head x' and 'warped Head y' columns.

    Returns:
    pandas.DataFrame: A DataFrame with the decision for each timepoint.
    """
    decisions = []
    decision = None
    
    for index, row in df.iterrows():
        x = row['warped Head x']
        y = row['warped Head y']
        
        if (decision != None) and y > 90: # 0>_000_0 Start of a new trial
            decision = None

        elif (decision == None) and y < 46: # entering T-entry
            decision = 'T-entry'

        elif decision == 'T-entry':
            if y > 50:  # 0_000_>0 (last + 1) frame of each trial
                decision = None
            elif x > 309:
                decision = 'Acc'
            elif x < 282:
                decision = 'Rej'

        elif decision == 'Acc' and x < 282:
            decision = 'quit'

        # Append the decision for the current row
        decisions.append(decision)

    # Add the decisions column to the DataFrame
    df['decision'] = decisions

    return df
