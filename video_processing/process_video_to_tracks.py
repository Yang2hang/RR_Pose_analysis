import os
from logger import setup_logger
from transform_coordinates import transform_coordinates
from smooth_data import smooth_data
from label_decision import label_decision
from get_kinematic_features import get_displacement
from get_kinematic_features import get_velocity
from get_kinematic_features import get_acceleration
from track_videos import track_videos
from convert_slp_files import convert_slp_files

def process_video_to_tracks(video_folder, model_path):
    # Logger setup
    logger_location = str(video_folder) + '/logger'
    if not os.path.isdir(logger_location):
        os.makedirs(logger_location)
    logger = setup_logger(str(video_folder).split('/')[-1], logger_location)
    
    # Track videos
    track_videos(video_folder, model_path, logger)

    # Convert SLEAP files
    convert_slp_files(video_folder, logger)
    
    

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
    
    for filename in os.listdir(video_folder):
        if filename.endswith('analysis.h5'):
            
            input_h5 = os.path.join(video_folder, filename)
            # Warp all coordinates to align the videos from different cameras
            df = transform_coordinates(input_h5, logger)
            
            
            smoothed_df = smooth_data(df, columns_to_smooth, logger)

            # label decisions
            labeled_df = label_decision(smoothed_df)
    
            displacement_df = get_displacement(labeled_df, bodyparts)
            velocity_df = get_velocity(displacement_df, bodyparts, frame_rate=30)
            acceleration_df = get_acceleration(velocity_df, bodyparts, frame_rate=30)

            acceleration_df.to_csv(str(filename).split('.')[0] + '.csv')
            
            logger.info(f'Preprocess done for: {str(filename).split('.')[0]}')
