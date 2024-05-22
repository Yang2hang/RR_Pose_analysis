import os
import subprocess

def track_videos(video_path, model_path):
    '''
    track videos (warped) under the input path with the input model
    '''
    # Analyze all videos under video_path
    for filename in os.listdir(video_path):
        if filename.endswith('.avi'):
            input_path = os.path.join(video_path, filename)

            # Build the command
            command = [
                'sleap-track',
                input_path,
                '-m',
                model_path
            ]

            # Run the command
            subprocess.run(command, check=True)

    print("Tracking complete for all videos.")
