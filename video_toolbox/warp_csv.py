import numpy as np
import pandas as pd
import cv2
from rr_sleap_track.transform_coordinates import get_warp_matrix

def warp_coordinates(csv_file):
    '''
    Apply affine transformation to the input CSV file to align with R2 camera orientation
    
    Return:
    a pandas DataFrame
    '''
    df = pd.read_csv(csv_file) 

    # Define the columns containing the coordinates
    coordinate_columns = [
        'Head x', 'Head y',
        'Neck x', 'Neck y',
        'Torso x', 'Torso y',
        'Tailhead x', 'Tailhead y'
    ]

    warped_columns = [
        'warped Head x', 'warped Head y',
        'warped Neck x', 'warped Neck y',
        'warped Torso x', 'warped Torso y',
        'warped Tailhead x', 'warped Tailhead y'
    ]

    for col in warped_columns:
        df[col] = 0

    for index, row in df.iterrows():
        coords = row[coordinate_columns].values.reshape(-1, 2)
        warp_matrix = get_warp_matrix(row['restaurant'])

        transformed_coords = cv2.transform(np.array([coords], dtype=np.float32), warp_matrix).reshape(-1)
        
        df.loc[index, warped_columns] = transformed_coords
    
    return df

csv = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/decision_thresholds.csv'
output_df = warp_coordinates(csv)
output_df.to_csv('/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/decision_thresholds.csv')
