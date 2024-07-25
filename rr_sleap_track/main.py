from rr_sleap_track.sleap_track import sleap_track
import sys
import os

# sys.path.append(os.path.join(os.getcwd().split(os.path.sep)))

# make sure the video name is RRM0xx_Dayxxx_Rx_turns.avi
# this program should run in sleap_env
# output raw_track files will be in raw_track folder in output_root_folder
sleap_video_root = r'/media/data/Sleap/testing_space'
model_path = r'/home/wholebrain/sleap_models/20240402_RR_n24/models/v003.6_240624_151538.single_instance.n=870'
output_root_folder = r'/media/data/Sleap/testing_space'
video_list = None

sleap_track(sleap_video_root, model_path, output_root_folder, video_list)