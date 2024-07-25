import numpy as np
import pandas as pd
import cv2

def get_warp_matrix(filename):
    '''
    Define warp matrix by the key points coordinates according to file names (camera location).
    3 key points are 3 corners of the restaurants.
    '''
    if 'R1' in str(filename):
        srcTri = np.array([[180.54, 140.24], [180.54, 176.96], [220.91, 176.35]]).astype(np.float32)
        dstTri = np.array([[64, 10], [74.9, 10], [74.9, 0.85]]).astype(np.float32)
    elif 'R2' in str(filename):
        srcTri = np.array([[220.3, 127.8], [267.55, 127.01], [167.23, 95.22]]).astype(np.float32)
        dstTri = np.array([[64, 10], [52.5, 10], [52.5, 0.7]]).astype(np.float32)
    elif 'R3' in str(filename):
        srcTri = np.array([[208.2, 93.7], [208.5, 50.34], [168.8, 50.6]]).astype(np.float32)
        dstTri = np.array([[64, 10], [52.9, 10], [52.9, 0.6]]).astype(np.float32)
    elif 'R4' in str(filename):
        srcTri = np.array([[160.63, 114.85], [106.7, 114.9], [107.2, 154.7]]).astype(np.float32)
        dstTri = np.array([[64, 10], [52.7, 10], [52.7, 0.8]]).astype(np.float32)
    else:
        return None

    warp_matrix = cv2.getAffineTransform(srcTri, dstTri)
    return warp_matrix

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

    # Extract the coordinates
    coords = df[coordinate_columns].values
    warp_matrix = get_warp_matrix(csv_file.split('/')[-1])

    # Apply affine transformation to each pair of coordinates
    transformed_coords = np.empty_like(coords)
    for i in range(0, coords.shape[1], 2): 
        points = coords[:, i:i+2]
        points = points.reshape(-1, 1, 2)
        transformed_points = cv2.transform(points, warp_matrix).reshape(-1, 2)

        transformed_coords[:, i:i+2] = transformed_points

    # Update the dataframe with the transformed and cropped coordinates
    df[warped_columns] = transformed_coords
    
    return df

csv = '/Users/yang/Documents/Wilbrecht_Lab/code/RR_Pose_analysis/video_toolbox/R4_decision_thresholds.csv'
output_df = warp_coordinates(csv)
output_df.to_csv('/Users/yang/Documents/Wilbrecht_Lab/code/RR_Pose_analysis/video_toolbox/R4_decision_thresholds_out.csv')
