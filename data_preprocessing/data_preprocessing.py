import os
import pandas as pd
from logger import setup_logger
from label_decision import label_decision
from get_kinematic_features import *
from label_trials import label_trials
from smooth_data import smooth_data

def data_preprocessing(root_video_folder):
    '''
    Access all _track_raw csv files, smooth the data and calculate the kinematic 
    parameters and output a csv file for each file (all output files are stored in 
    a different folder in the root video folder).
    '''
    
    # Create the preprocessed_data folder in the root video folder
    preprocessed_data_folder = os.path.join(root_video_folder, 'preprocessed_data')
    if not os.path.isdir(preprocessed_data_folder):
        os.makedirs(preprocessed_data_folder)
    
    # Logger setup
    logger_location = os.path.join(preprocessed_data_folder, 'logger')
    if not os.path.isdir(logger_location):
        os.makedirs(logger_location)
    logger = setup_logger(os.path.basename(root_video_folder), logger_location)

    # Warped columns to be smoothed
    columns_to_smooth = [
        'warped Head x', 'warped Head y',
        'warped Neck x', 'warped Neck y',
        'warped Torso x', 'warped Torso y',
        'warped Tailhead x', 'warped Tailhead y'
    ]
    
    # Bodyparts to calculate velocity
    bodyparts = [
        'Head',
        'Neck',
        'Torso',
        'Tailhead'
    ]
    
    # Walk through all subdirectories in the root video folder
    for root, dirs, files in os.walk(root_video_folder):
        for subdir in dirs:
            
            subdir_path = os.path.join(root, subdir)
            
            for filename in os.listdir(subdir_path):
                if filename.endswith('_tracks_raw.csv'):
                    raw_filepath = os.path.join(subdir_path, filename)
                    raw_df = pd.read_csv(raw_filepath)
                    
                    smoothed_df = smooth_data(raw_df, columns_to_smooth, logger)
                    
                    labeled_t_df = label_trials(smoothed_df, filename)
                    labeled_d_df = label_decision(labeled_t_df)
                    
                    displacement_df = get_displacement(labeled_d_df, bodyparts)
                    velocity_df = get_velocity(displacement_df, bodyparts, frame_rate=30)
                    acceleration_df = get_acceleration(velocity_df, bodyparts, frame_rate=30)
                    
                    # Assign the output path in the preprocessed_data folder
                    parts = filename.split('_')
                    base = '_'.join(parts[:3])
                    output_subdir = os.path.join(preprocessed_data_folder, subdir)
                    if not os.path.isdir(output_subdir):
                        os.makedirs(output_subdir)
                    output_path = os.path.join(output_subdir, base + '_processed.csv')
                    
                    acceleration_df.to_csv(output_path)
                    
                    logger.info(f'Preprocess done for: {base}')

