import os
import shutil

def reorganize_directory_structure(root):
    '''
    iterate the animal folders containing different files and saperate them into following folders in the root dir.
    root/
    ├── RRM030/
    │   ├── Day150/
    │   │   ├── _tracks_raw.csv
            ├── .slp
            ├── .h5
            ├── ...
    
    the root folder should contain animal folders named like 'RRM030', animal
    raw_track folder: contain raw track csv files
    intermediate_track_files folder: contain predictions.slp and analysis.h5 files
    '''
    raw_track_dir = os.path.join(root, 'raw_track')
    sleap_intermediate_dir = os.path.join(root, 'intermediate_track_files')
    
    # Ensure the new directories exist
    if not os.path.exists(raw_track_dir):
        os.makedirs(raw_track_dir)
    if not os.path.exists(sleap_intermediate_dir):
        os.makedirs(sleap_intermediate_dir)
    
    for animal in os.listdir(root):
        animal_path = os.path.join(root, animal)
        if os.path.isdir(animal_path) and animal.startswith('RRM'):
            for session in os.listdir(animal_path):
                session_path = os.path.join(animal_path, session)
                if os.path.isdir(session_path) and session.startswith('Day'):
                    for file in os.listdir(session_path):
                        file_path = os.path.join(session_path, file)
                        # Move files to appropriate directories
                        if file.endswith('_tracks_raw.csv'):
                            new_session_dir = os.path.join(raw_track_dir, animal, session)
                            if not os.path.exists(new_session_dir):
                                os.makedirs(new_session_dir)
                            shutil.move(file_path, os.path.join(new_session_dir, file))
                        elif file.endswith('_analysis.h5') or file.endswith('predictions.slp'):
                            new_session_dir = os.path.join(sleap_intermediate_dir, animal, session)
                            if not os.path.exists(new_session_dir):
                                os.makedirs(new_session_dir)
                            shutil.move(file_path, os.path.join(new_session_dir, file))

root_directory = r'/Users/yang/Documents/Wilbrecht_Lab/sleap_video'
reorganize_directory_structure(root_directory)