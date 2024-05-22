import os
import subprocess

def convert_slp_files(video_path):
    '''
    Convert all .slp files into .h5 files
    '''
    for filename in os.listdir(video_path):
        if filename.endswith('predictions.slp'):
            input_video = os.path.join(video_path, filename)
            base, _ = os.path.splitext(filename)
            output_path = os.path.join(video_path, base + '.analysis.h5')

            # Build the command
            command = [
                'sleap-convert',
                input_video,
                '--format', 'analysis',
                '-o', output_path
            ]

            # Run the command
            subprocess.run(command, check=True)

    print("Convert complete for all files.")
