import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.signal import find_peaks

from process_video_to_tracks import process_video_to_tracks
from transform_coordinates import transform_coordinates
from smooth_data import smooth_data
from label_decision import label_decision
from trial_analysis import trial_analysis
from get_kinematic_features import get_displacement
from get_kinematic_features import get_velocity
from get_kinematic_features import get_acceleration

def process_video_to_tracks(h5_folder):
    # Warp all coordinates to align the videos from different cameras
    df = transform_coordinates(h5_folder)

    # Smooth the data
    columns_to_smooth = [
        'warped Head x', 'warped Head y',
        'warped Neck x', 'warped Neck y',
        'warped Torso x', 'warped Torso y',
        'warped Tailhead x', 'warped Tailhead y'
    ]
    smoothed_df = smooth_data(df, columns_to_smooth)

    # label decisions
    labeled_df = label_decision(smoothed_df)
    
    # calculate velocity
    bodyparts = [
        'Head',
        'Neck',
        'Torso',
        'Tailhead'
    ]

    displacement_df = get_displacement(labeled_df, bodyparts)
    velocity_df = get_velocity(displacement_df, bodyparts, frame_rate=30)
    acceleration_df = get_acceleration(velocity_df, bodyparts, frame_rate=30)
    
    return acceleration_df


