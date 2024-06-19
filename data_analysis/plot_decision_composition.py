import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

def plot_decision_composition(df, column, window_size=50, step_size=10, x_range=None):
    """
    Plots the composition of different decisions in different average speed intervals using a line graph with SEM.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing 'average_speed' and 'final_decision' columns.
    window_size (int): The size of the speed window.
    step_size (int): The step size for the sliding window.
    """
    # Create a copy of the DataFrame to avoid modifying the original DataFrame
    df_copy = df.copy()

    # Define speed intervals using a sliding window
    max_speed = df_copy[column].max()
    min_speed = df_copy[column].min()
    speed_intervals = np.arange(min_speed, max_speed + step_size, step_size)

    proportions = []
    for i in range(len(speed_intervals) - 1):
        lower_bound = speed_intervals[i]
        upper_bound = lower_bound + window_size
        interval_data = df_copy[(df_copy[column] >= lower_bound) & (df_copy[column] < upper_bound)]
        
        if len(interval_data) > 0:
            interval_composition = interval_data['final decision'].value_counts(normalize=True)
            proportions.append(interval_composition)
        else:
            proportions.append(pd.Series(dtype=float))
    
    # Create a DataFrame for the proportions
    proportions_df = pd.DataFrame(proportions, index=speed_intervals[:-1])
    
    # Plot the line graph with SEM error bars
    plt.figure(figsize=(10, 6))
    for decision in proportions_df.columns:
        proportion = proportions_df[decision]
        plt.plot(proportions_df.index, proportion, label=decision)
    
    plt.xlabel(column)
    plt.ylabel('Proportion of Decisions')
    plt.title(f'Decisions Composition over {column} Intervals')
    plt.legend(title='Decision')
    plt.grid(True)
    if x_range is not None:
        plt.xlim(x_range)
    plt.tight_layout()
    plt.show()