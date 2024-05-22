import numpy as np
import pandas as pd

def triangular_moving_average(y, window_size=5):
    '''
    Parameters:
        y: time series data (list or numpy array)
        window_size: size of the triangular moving average window (must be odd)

    Output:
        smoothed_data_series: Series with smoothed time series data
        
    by Cameron
    '''

    assert window_size % 2 == 1, "the window size must be odd"

    # Create the triangular window
    window = np.concatenate((np.arange(1, (window_size + 1) // 2 + 1), 
                             np.arange((window_size + 1) // 2 - 1, 0, -1)))
    window = window / window.sum()
    
    # Pad the data at the edges
    padded_data = np.pad(y, (window_size // 2, window_size // 2), mode='edge')
    
    # Convolve the padded data with the window
    smoothed_data = np.convolve(padded_data, window, mode='valid')

    # Create a Series with the smoothed data
    smoothed_data_series = pd.Series(smoothed_data, name='Smoothed Data')
    
    return smoothed_data_series

