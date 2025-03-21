# RR_Pose_analysis
Restaurant Row Project in Wilbrecht Lab
Note: The folder_path parameter in the following program should be set to the root folder which contains animal folders. animal folder should contain session folders.
## Pipeline
### In sleap environment:
1. Set the correct root_video_folder and model path. Then run sleap_track/main.py.
2. Set the root_directory (same as the folder in sleap_track) and then run reorganize_dir.py to sort the intermidiate track results into different folders.

### In another environment with updated scipy:
1. Set the raw_track folder created by sleap_track.py as the input. Then run data_preprocessing/main.py. The processed data is in raw_track/processed_tracks folder.
2. Run combine_raw_tracks.py and this will integrate all tracks_processed.csv files into one super DataFrame:'combined_df', and save it in processed_data folder for further analysis.

### Data cleaning
1. get_df_wide.ipynb: data cleaning and calculate trial wise features -> trial_df
2. trajectory_clustering.ipynb: do dim red and clustering on tracks -> cluster_df