import os
import pandas as pd

def append_time_info(df, video_folder, filename):
    """
    Appends specific columns from a CSV file to the input DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to which columns will be appended.
    - video_folder (str): The directory where the CSV file is located.
    - h5_file (str): The H5 file name, which determines the CSV file name.

    Returns:
    - pd.DataFrame: The DataFrame with the appended columns.
    """
    # Construct the CSV file name based on the H5 file name
    csv_file_name = filename.split('.')[0] + '.csv'
    csv_file_path = os.path.join(video_folder, csv_file_name)

    if not os.path.exists(csv_file_path):
        print(f"CSV file {csv_file_path} does not exist.")
        return df

    # Read the CSV file into a DataFrame
    csv_df = pd.read_csv(csv_file_path)

    # Extract the specified columns
    columns_to_extract = ['time', 'idx', 'label', 'rel_time', 'restaurant', 'lapIndex', 'trial']
    extracted_df = csv_df[columns_to_extract]

    # Check if the number of rows match
    if len(df) != len(extracted_df):
        print("The number of rows in the input DataFrame and the CSV file do not match.")
        return df

    # Append the columns to the input DataFrame
    appended_df = pd.concat([df, extracted_df], axis=1)

    return appended_df
