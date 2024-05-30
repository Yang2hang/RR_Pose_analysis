import os
import subprocess

def track_videos(video_path, model_path, logger):
    '''
    track videos (warped) under the input path with the input model and output a 
    sleap prediction file ('_predictions.slp') for each video file
    '''
    # Analyze all videos under video_path
    for filename in os.listdir(video_path):
        if filename.endswith('.avi'):
            input_path = os.path.join(video_path, filename)
            logger.info(f"Processing video: {filename}")

            # Build the command
            command = [
                'sleap-track',
                input_path,
                '-m',
                model_path
            ]

            # Run the command
            try:
                subprocess.run(command, check=True)
                logger.info(f"Successfully processed. output: {filename + '.predictions.slp'}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error processing {filename}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error processing {filename}: {e}")

    logger.info("---Tracking complete for all videos.---")