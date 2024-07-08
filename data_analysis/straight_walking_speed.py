import pandas as pd
import matplotlib.pyplot as plt

def straight_walking_speed(df, speed_threshold=500):
    """
    Extracts the straight walking speed (before T-entry) for each trial.
    
    Parameters:
    df (pandas.DataFrame): The input DataFrame with columns 'Elapsed Time', 'decision', and 'Head velocity'.
    
    Returns:
    list: A list of DataFrames, each containing the straight walking speed for one trial.
    """
    trials = []
    current_trial = []
    in_trial = False

    for index, row in df.iterrows():
        decision = row['decision']
        speed = np.sqrt(row['Head velocity x']**2 + row['Head velocity y']**2)


        if decision == 'T-entry' and in_trial:
            # End the current trial at T-entry
            if current_trial:
                trials.append(pd.DataFrame({'speed': current_trial[1:]}))
            current_trial = []
            in_trial = False

        if decision is None:
            in_trial = True
            if speed < speed_threshold:
                current_trial.append(speed)
                
    # Append the last trial if it was not followed by a T-entry
    if current_trial:
        trials.append(pd.DataFrame({'speed': current_trial}))

    return trials

def plot_straight_walking_speed(trials):
    """
    Plots the straight walking speed for each trial.
    
    Parameters:
    trials (list): A list of DataFrames, each containing the straight walking speed for one trial.
    """
    plt.figure(figsize=(12, 6))

    for i, trial in enumerate(trials):
        if not trial.empty:
            velocity = trial['speed']
            plt.plot(velocity, label=f'Trial {i+1}')

    plt.xlabel('Time')
    plt.ylabel('Head Velocity (units/s)')
    plt.title('Instantaneous Straight Walking Speed Before T-entry')
    plt.grid(True)
    plt.show()
