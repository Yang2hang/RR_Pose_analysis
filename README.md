# RR_Pose_analysis
Restaurant Row Project in Wilbrecht Lab
Note: The folder_path parameter in the following program should be set as the 
Pipeline
In sleap environment:
1. Set the correct root_video_folder and model path. Then run sleap_track/main.py.
2. Set the root_directory (same as the folder in sleap_track) and then run reorganize_dir.py to sort the track results into different folders.

In another environment with updated scipy:
1. Set the raw_track folder created by sleap_track.py as the input. Then run data_preprocessing/main.py. The processed data is in raw_track/preprocessed_data folder.
2. Run integrate_super_df.ipynb. This will integrate all _processed.csv files into one super DataFrame:'combined_df', and save it in processed_data folder for further analysis.

Data analysis
1. Run data_analysis/main.ipynb
2. Run trajectory_clustering.ipynb