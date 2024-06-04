import os
from sleap_track import sleap_track

# make sure the video name is RRM0xx_Dayxxx_Rx_turns.avi
# this program should run in sleap_env
root_video_folder = '/home/wholebrain/sleap_models/20240402_RR_n24/Videos'
model_path = '/home/wholebrain/sleap_models/20240402_RR_n24/models/v003.3_240430_165906.single_instance.n=732'

sleap_track(root_video_folder, model_path)