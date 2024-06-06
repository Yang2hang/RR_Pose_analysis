import os
import shutil

def reorganize_directory_structure(root):
    raw_track_dir = os.path.join(root, 'raw_track')
    sleap_intermediate_dir = os.path.join(root, 'intermediate_track_files')
    
    # Ensure the new directories exist
    if not os.path.exists(raw_track_dir):
        os.makedirs(raw_track_dir)
    if not os.path.exists(sleap_intermediate_dir):
        os.makedirs(sleap_intermediate_dir)
    
    for subdir in os.listdir(root):
        subdir_path = os.path.join(root, subdir)
        if os.path.isdir(subdir_path) and subdir.startswith('RRM'):
            for session_folder in os.listdir(subdir_path):
                session_folder_path = os.path.join(subdir_path, session_folder)
                if os.path.isdir(session_folder_path) and session_folder.startswith('Day'):
                    for file in os.listdir(session_folder_path):
                        file_path = os.path.join(session_folder_path, file)
                        if os.path.isfile(file_path):
                            # Create new session directory paths
                            new_raw_track_dir = os.path.join(raw_track_dir, subdir, session_folder)
                            new_sleap_intermediate_dir = os.path.join(sleap_intermediate_dir, subdir, session_folder)
                            
                            # Move files to appropriate directories
                            if file.endswith('_tracks_raw.csv'):
                                if not os.path.exists(new_raw_track_dir):
                                    os.makedirs(new_raw_track_dir)
                                shutil.move(file_path, os.path.join(new_raw_track_dir, file))
                            elif file.endswith('_analysis.h5') or file.endswith('predictions.slp'):
                                if not os.path.exists(new_sleap_intermediate_dir):
                                    os.makedirs(new_sleap_intermediate_dir)
                                shutil.move(file_path, os.path.join(new_sleap_intermediate_dir, file))
                            else:
                                pass

root_directory = '/Users/yang/Documents/Wilbrecht_Lab/sleap_video'
reorganize_directory_structure(root_directory)
