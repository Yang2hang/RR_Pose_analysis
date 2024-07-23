import os
from track_processing import track_processing

# make sure the csv name is RRM0xx_Dayxxx_Rx_tracks_raw.csv
# this program should run in another env with updated scipy
# root_video_folder should be the raw_track folder from reorganize_dir.py, all results will be stored in raw_track/processed_tracks
track_root = r'/Users/yang/Documents/Wilbrecht_Lab/data/raw_track'

track_processing(track_root)