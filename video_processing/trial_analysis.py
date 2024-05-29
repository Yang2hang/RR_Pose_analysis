import numpy as np
import pandas as pd

def trial_analysis(df):
    """
    Extracts the final decision for each trial from the labeled DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing the labeled data with decisions.

    Returns:
    pandas.DataFrame: A DataFrame with each row representing a trial, containing columns
                      for the trial number and the final decision.
    """
    final_decisions = []
    trial_num = 0
    current_decision = None

    for index, row in df.iterrows():
        y = row['warped Head y']
        decision = row['decision']

        if current_decision is not None and y > 90:  # 0_000_>0 End of current trial and start of a new trial
            final_decisions.append({'trial_num': trial_num, 'final_decision': current_decision})
            trial_num += 1
            current_decision = None

        if decision is not None:
            current_decision = decision

    # Handle the final trial if it doesn't end with y > 90
    if current_decision is not None:
        final_decisions.append({'trial_num': trial_num, 'final_decision': current_decision})

    return pd.DataFrame(final_decisions)