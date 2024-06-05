import os
from data_preprocessing import data_preprocessing

# make sure the csv name is RRM0xx_Dayxxx_Rx_tracks_raw.csv
# this program should run in another env
root_video_folder = r'/Users/yang/Documents/Wilbrecht_Lab/sleap_video'

data_preprocessing(root_video_folder)