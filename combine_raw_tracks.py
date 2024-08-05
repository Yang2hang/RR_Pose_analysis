import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import join as oj

root_folder = '/Users/yang/Documents/Wilbrecht_Lab/data/processed_tracks'


# Following code block is used to generate a super DaraFrame containing all animals and sessions in the root folder
# Get all animal folders

animal_folder_paths = [oj(root_folder, animal) for animal in os.listdir(root_folder) if (os.path.isdir(oj(root_folder, animal)) and animal.startswith('RRM'))]

# Collect and plot all data
dataframes = []
for animal_folder_path in animal_folder_paths:
    animal = os.path.basename(animal_folder_path)
    # Get all session folders
    for session in os.listdir(animal_folder_path):
        animal_dfs = []
        session_path = oj(animal_folder_path, session)
        if os.path.isdir(session_path):
            for filename in os.listdir(session_path):
                if filename.startswith(f'{animal}_{session}') and filename.endswith('tracks_processed.csv'):
                    file_path = oj(session_path, filename)
                    df = pd.read_csv(file_path, index_col=False)
                    df['animal'] = animal
                    df['session'] = session
                    animal_dfs.append(df)
                    dataframes.append(df)
            animal_df = pd.concat(animal_dfs) 
            #plot_two_column(animal_df, animal, session, 'time', 'warped Head y')
            #plot_trajectory(animal_df, animal, session)

# Combine all data into a single dataframe
combined_df = pd.concat(dataframes)

combined_df.to_csv(oj(root_folder, 'combined_df.csv'), index=False)