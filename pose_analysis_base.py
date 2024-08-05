from os.path import join as oj
import os
import pandas as pd
import numpy as np

class PoseMat:
    def __init__(self, root_folder, combined_file='combined_df.csv'):
        self.root_folder = root_folder
        self.combined_file_path = oj(root_folder, combined_file)
        self.combined_df = None

    def get_animal(self, animal, session=None):
        animal_folder = oj(self.root_folder, animal)
        dataframes = []

        if os.path.isdir(animal_folder):
            if session:
                session_folder = oj(animal_folder, session)
                if os.path.isdir(session_folder):
                    for filename in os.listdir(session_folder):
                        if filename.startswith(f'{animal}_{session}') and filename.endswith('tracks_processed.csv'):
                            file_path = oj(session_folder, filename)
                            df = pd.read_csv(file_path, index_col=False)
                            df['animal'] = animal
                            df['session'] = session
                            dataframes.append(df)
                else:
                    print(f'No matching session folder found for session: {session}.')

            # return all sessions if only animal is specified
            else:
                session_folders = [oj(animal_folder, s) for s in os.listdir(animal_folder) if os.path.isdir(oj(animal_folder, s))]
                for session_folder in session_folders:
                    session = os.path.basename(session_folder)
                    for filename in os.listdir(session_folder):
                        if filename.startswith(f'{animal}_{session}') and filename.endswith('tracks_processed.csv'):
                            file_path = oj(session_folder, filename)
                            df = pd.read_csv(file_path, index_col=False)
                            df['animal'] = animal
                            df['session'] = session
                            dataframes.append(df)
        else:
            print('No matching animal folder found.')

        if dataframes:
            combined_df = pd.concat(dataframes, axis=0, ignore_index=True).reset_index(drop=True)
            return combined_df
        else:
            if session:
                print(f'No data files found for animal {animal} in session {session}.')
            else:
                print(f'No data files found for animal {animal}.')
            return None

    def _generate_combined_df(self):
        animal_folder_paths = [oj(self.root_folder, animal) for animal in os.listdir(self.root_folder)
                               if os.path.isdir(oj(self.root_folder, animal)) and animal.startswith('RRM')]

        dataframes = []
        for animal_folder_path in animal_folder_paths:
            animal = os.path.basename(animal_folder_path)
            for session in os.listdir(animal_folder_path):
                session_path = oj(animal_folder_path, session)
                if os.path.isdir(session_path):
                    for filename in os.listdir(session_path):
                        if filename.startswith(f'{animal}_{session}') and filename.endswith('tracks_processed.csv'):
                            file_path = oj(session_path, filename)
                            df = pd.read_csv(file_path, index_col=False)
                            df['animal'] = animal
                            df['session'] = session
                            dataframes.append(df)
        
        if dataframes:
            combined_df = pd.concat(dataframes, axis=0, ignore_index=True).reset_index(drop=True)
            combined_df.to_csv(self.combined_file_path, index=False)
            self.combined_df = combined_df
        else:
            print('No data files found to generate combined DataFrame.')

    def _load_combined_df(self):
        if os.path.isfile(self.combined_file_path):
            self.combined_df = pd.read_csv(self.combined_file_path, index_col=False)
        else:
            print(f'Combined file {self.combined_file_path} not found.')

    def get_combined_df(self):
        if self.combined_df is None:
            if os.path.isfile(self.combined_file_path):
                print('Loading combined DataFrame...')
                self._load_combined_df()
            else:
                print('Combined file not found. Generating...')
                self._generate_combined_df()
        return self.combined_df
    
    
class TrialMat:
    def __init__(self, root_folder, trial_file='trial_df.csv'):
        self.root_folder = root_folder
        self.trial_file_path = oj(self.root_folder, trial_file)
        self.trial_df = None

    def _generate_trial_df(self, combined_df, length):
        current_trial_num = np.nan
        current_session = np.nan
        current_animal = np.nan
        current_decision = np.nan
        current_restaurant = np.nan
        decision = np.nan
        current_length = 0
        sum_of_speed = 0
        speed_count = 0

        decision_list = []
        straight_walking_speed_list = []
        animal_list = []
        session_list = []
        trial_list = []
        trial_lengths = []
        current_trial_coords = []
        trial_13_coords = []

        for index, row in combined_df.iterrows():
            decision = row['decision']
            trial_num = row['trial']
            animal = row['animal']
            session = row['session']
            speed = np.sqrt(row['Head_vx']**2 + row['Head_vy']**2)
            restaurant = row['restaurant']
            head_x = row['warped Head x']
            head_y = row['warped Head y']

            if trial_num != current_trial_num:  # Start of a new trial
                if speed_count != 0:
                    average_speed = sum_of_speed / speed_count
                else:
                    average_speed = np.nan

                if not np.isnan(current_trial_num) and (len(current_trial_coords) >= length * 2):
                    trial_13_coords.append(current_trial_coords[:(length * 2)])
                    decision_list.append(current_decision)
                    straight_walking_speed_list.append(average_speed)
                    animal_list.append(current_animal)
                    session_list.append(current_session)
                    trial_list.append(current_trial_num)
                    trial_lengths.append(current_length)

                current_restaurant = restaurant
                current_decision = np.nan
                current_trial_num = trial_num
                current_session = session
                current_animal = animal
                sum_of_speed = 0
                speed_count = 0
                current_length = 1
                current_trial_coords = [head_x, head_y]
            else:  # Within trial
                current_length += 1
                current_trial_coords.append(head_x)
                current_trial_coords.append(head_y)

            if not pd.isna(decision):  # Decision != None
                current_decision = decision

            if pd.isna(current_decision) and (speed < 300):  # Straight walking speed
                sum_of_speed += speed
                speed_count += 1

        coord_columns = [f'x{i // 2 + 1}' if i % 2 == 0 else f'y{i // 2 + 1}' for i in range(self.length * 2)]
        coords_df = pd.DataFrame(trial_13_coords, columns=coord_columns)

        other_df = pd.DataFrame({
            'sleap_decision': decision_list,
            'straight_walking_speed': straight_walking_speed_list,
            'animal': animal_list,
            'session': session_list,
            'trial': trial_list,
            'trial_length': trial_lengths,
        })

        result_df = pd.concat([coords_df, other_df], axis=1)
        return result_df

    def get_trial_df(self, length=32):
        """
        Load or generate the trial DataFrame.

        Parameters:
        length (int): The length of coordinates to be used in the trial DataFrame.

        Returns:
        pd.DataFrame: The trial DataFrame.
        """
        if os.path.isfile(self.trial_file_path):
            print('Loading trial DataFrame...')
            self.trial_df = pd.read_csv(self.trial_file_path, index_col=False)
        
        else:
        # trial DataFrame not exist    
            combined_df_path = oj(self.root_folder, 'combined_df.csv')
            if os.path.isfile(combined_df_path):
                print('Generating trial DataFrame from combined DataFrame')
                combined_df = pd.read_csv(combined_df_path)
                self.trial_df = self._generate_trial_df(combined_df, length)
                self.trial_df.to_csv(self.trial_file_path, index=False)
            else:
                print("No combined DataFrame available to calculate trial DataFrame.")
        return self.trial_df
    
    def get_filtered_trials(self, condition_func):
        """
        Filter the trials based on the given condition function.

        Parameters:
        condition_func (function): A function that takes decision, average_speed, restaurant, animal, session, trial_num as parameters
                                   and returns a boolean indicating if the trial satisfies the condition.

        Returns: 
        pd.DataFrame: The filtered DataFrame.
        """
        if self.trial_df is None:
            self.get_trial_df()

        filtered_df = self.trial_df[self.trial_df.apply(
            lambda row: condition_func(
                row['bonsai_decision'],
                row['sleap_decision'],
                row['straight_walking_speed'],
                row['restaurant'],
                row['animal'],
                row['session'],
                row['trial']
            ), axis=1)]
        return filtered_df
        