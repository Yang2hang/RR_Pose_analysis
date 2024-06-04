import os
from data_preprocessing import data_preprocessing

# make sure the csv name is RRM0xx_Dayxxx_Rx_tracks_raw.csv
# this program should run in another env
root_video_folder = '/home/wholebrain/sleap_models/20240402_RR_n24/Videos'

data_preprocessing(root_video_folder)