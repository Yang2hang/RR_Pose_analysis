import os
from data_preprocessing import data_preprocessing

# make sure the csv name is RRM0xx_Dayxxx_Rx_tracks_raw.csv
# this program should run in another env with updated scipy
# root_video_folder should be the raw_track folder from reorganize_dir.py, all results will be stored in raw_track/processed_tracks
root_video_folder = r'/Users/yang/Documents/Wilbrecht_Lab/data4analysis/raw_track'

data_preprocessing(root_video_folder)