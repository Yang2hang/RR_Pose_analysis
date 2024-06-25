import os
import shutil


def migrate_csv_files(source_root, target_root):
    not_existing_files = []

    for animal_folder in os.listdir(source_root):
        source_animal_path = os.path.join(source_root, animal_folder)
        target_animal_path = os.path.join(target_root, animal_folder)
        if not os.path.isdir(target_animal_path):
            print(f'{target_animal_path} does not exist')
        if os.path.isdir(source_animal_path):
            for session_folder in os.listdir(source_animal_path):
                source_session_path = os.path.join(source_animal_path, session_folder)
                target_session_path = os.path.join(target_animal_path, session_folder)
                if not os.path.isdir(target_session_path):
                    print(f'{target_session_path} does not exist')
                if os.path.isdir(source_session_path):
                    for csv_file in os.listdir(source_session_path):
                        if csv_file.endswith('_tracks_raw.csv'):
                            source_csv_path = os.path.join(source_session_path, csv_file)
                            target_csv_path = os.path.join(target_session_path, csv_file)

                            if os.path.exists(target_csv_path):
                                shutil.copy2(source_csv_path, target_csv_path)
                            else:
                                print(f'{csv_file} does not exist in target folder.')

source_root = '/media/data/Sleap/raw_track'
target_root = '/media/server/Restaurant Row/Data/ARJ_raw'

migrate_csv_files(source_root, target_root)
