import os
from process_video_to_tracks import process_video_to_tracks

video_folder = '/home/wholebrain/sleap_models/20240402_RR_n24/Videos'
model_path = '/home/wholebrain/sleap_models/20240402_RR_n24/models/v003.3_240430_165906.single_instance.n=732'

process_video_to_tracks(video_folder, model_path)