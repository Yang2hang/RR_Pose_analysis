import os
import shutil

def reorganize_directory_structure(root):
    '''
    iterate the animal folders in root folder containing different files and saperate them into following folders in the root dir.
    root_folder:
    root/
    ├── RRM030/
    │   ├── Day150/
    │   │   ├── .slp
    │   │   ├── .h5
    │   │   ├── ...
    
    intermediate_track_files folder: contain predictions.slp and analysis.h5 files
    '''
    sleap_intermediate_dir = os.path.join(root, 'intermediate_track_files')
    
    # Ensure the new directories exist
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
                        if file.endswith('_analysis.h5') or file.endswith('predictions.slp'):
                            new_session_dir = os.path.join(sleap_intermediate_dir, animal, session)
                            if not os.path.exists(new_session_dir):
                                os.makedirs(new_session_dir)
                            shutil.move(file_path, os.path.join(new_session_dir, file))

root_directory = r'/Users/yang/Documents/Wilbrecht_Lab/sleap_video'
reorganize_directory_structure(root_directory)