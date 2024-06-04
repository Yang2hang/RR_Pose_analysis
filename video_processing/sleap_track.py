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
    logger_location = str(video_folder) + '/logger'
    if not os.path.isdir(logger_location):
        os.makedirs(logger_location)
    logger = setup_logger(str(video_folder).split('/')[-1], logger_location)
    
    # Track videos
    track_videos(video_folder, model_path, logger)

    # Convert SLEAP files
    convert_slp_files(video_folder, logger)

    
    for filename in os.listdir(video_folder):
        if filename.endswith('analysis.h5'):
            
            input_h5 = os.path.join(video_folder, filename)
            # Warp all coordinates to align the videos from different cameras
            df = transform_coordinates(input_h5, logger)
            
            appended_df = append_time_info(df, video_folder, filename, logger)

            # Assign the output path
            parts = filename.split('_')
            base = '_'.join(parts[:3])
            output_path = os.path.join(video_folder, base + '_tracks_raw.csv')
            
            appended_df.to_csv(output_path)
            
            logger.info(f'Preprocess done for: {str(filename).split(".")[0]}')

