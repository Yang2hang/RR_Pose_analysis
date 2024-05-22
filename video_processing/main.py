import os
from track_videos import track_videos
from convert_slp_files import convert_slp_files

video_folder = '/home/wholebrain/sleap_models/20240402_RR_n24/Videos'
model_path = '/home/wholebrain/sleap_models/20240402_RR_n24/models/v003.3_240430_165906.single_instance.n=732'

# Track videos
track_videos(video_folder, model_path)

# Convert SLEAP files
convert_slp_files(video_folder)