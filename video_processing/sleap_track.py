import os
from logger import setup_logger
from transform_coordinates import transform_coordinates
from track_videos import track_videos
from convert_slp_files import convert_slp_files
from append_time_info import append_time_info

def sleap_track(video_folder, model_path):
    '''
    Track all videos under the input folder with the assigned model. Then output a '_predictions.slp' file and an 
    '_analysis.h5' file for each video. Then warp the coordinates and output a csv file for each video.
    '''
    
    # Logger setup
    logger_location = os.path.join(video_folder, 'logger')
    if not os.path.isdir(logger_location):
        os.makedirs(logger_location)
    logger = setup_logger(os.path.basename(video_folder), logger_location)
    
    # Walk through all subdirectories in the video_folder
    for root, dirs, files in os.walk(video_folder):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            
            # Track videos
            track_videos(subdir_path, model_path, logger)

            # Convert SLEAP files
            convert_slp_files(subdir_path, logger)

            for filename in os.listdir(subdir_path):
                if filename.endswith('analysis.h5'):
                    input_h5 = os.path.join(subdir_path, filename)
                    
                    # Warp all coordinates to align the videos from different cameras
                    df = transform_coordinates(input_h5, logger)
                    
                    appended_df = append_time_info(df, subdir_path, filename, logger)

                    # Assign the output path
                    parts = filename.split('_')
                    base = '_'.join(parts[:3])
                    output_path = os.path.join(subdir_path, base + '_tracks_raw.csv')
                    
                    appended_df.to_csv(output_path)
                    
                    logger.info(f'Preprocess done for: {filename}')