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
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                if os.path.isfile(file_path):
                    # Extract session information (e.g., Day123)
                    parts = file.split('_')
                    for part in parts:
                        if part.startswith('Day'):
                            session = part
                            break
                    else:
                        continue

                    # Create session directory if it doesn't exist
                    session_dir = os.path.join(subdir_path, session)
                    if not os.path.exists(session_dir):
                        os.makedirs(session_dir)

                    # Move files to appropriate directories
                    if file.endswith('_tracks_raw.csv'):
                        new_session_dir = os.path.join(raw_track_dir, subdir, session)
                        if not os.path.exists(new_session_dir):
                            os.makedirs(new_session_dir)
                        shutil.move(file_path, os.path.join(new_session_dir, file))
                    elif file.endswith('_analysis.h5') or file.endswith('predictions.slp'):
                        new_session_dir = os.path.join(sleap_intermediate_dir, subdir, session)
                        if not os.path.exists(new_session_dir):
                            os.makedirs(new_session_dir)
                        shutil.move(file_path, os.path.join(new_session_dir, file))
                    else:
                        shutil.move(file_path, os.path.join(session_dir, file))

root_directory = r'/Users/yang/Documents/Wilbrecht_Lab/sleap_video'
reorganize_directory_structure(root_directory)