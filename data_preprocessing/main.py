import os
from data_preprocessing import data_preprocessing

# make sure the csv name is RRM0xx_Dayxxx_Rx_tracks_raw.csv
# this program should run in another env with updated scipy
# run in raw_track folder from reorganize_dir.py, all results will be in raw_track/preprocessed_data
root_video_folder = r'/Users/yang/Documents/Wilbrecht_Lab/sleap_video/raw_track'

data_preprocessing(root_video_folder)