import cv2
import numpy as np
import pandas as pd
import os
from rr_sleap_track.h5_preprocessing import h5_preprocessing


def get_warp_matrix(filename, logger=None):
    '''
    Define warp matrix by the key points coordinates according to file names (camera location).
    3 key points are 3 corners of the restaurants.
    
    srcTri is the pixel coords
    dstTri is the real physical distance (unit: mm)
    '''
    try:
        if 'R1' in str(filename):
            srcTri = np.array([[180.54, 140.24], [180.54, 176.96], [220.91, 176.35]]).astype(np.float32)
            dstTri = np.array([[640, 100], [749, 100], [749, 8.5]]).astype(np.float32)
        elif 'R2' in str(filename):
            srcTri = np.array([[220.3, 127.8], [267.55, 127.01], [267.23, 95.22]]).astype(np.float32)
            dstTri = np.array([[640, 100], [755, 100], [755, 7]]).astype(np.float32)
        elif 'R3' in str(filename):
            srcTri = np.array([[208.2, 93.7], [208.5, 50.34], [168.8, 50.6]]).astype(np.float32)
            dstTri = np.array([[640, 100], [751, 100], [751, 6]]).astype(np.float32)
        elif 'R4' in str(filename):
            srcTri = np.array([[160.63, 114.85], [106.7, 114.9], [107.2, 154.7]]).astype(np.float32)
            dstTri = np.array([[640, 100], [753, 100], [753, 8]]).astype(np.float32)
        else:
            logger.error(f"Cannot find warp matrix for this file: {filename}")
            return None

        warp_matrix = cv2.getAffineTransform(srcTri, dstTri)
        return warp_matrix
    except Exception as e:
        if logger:
            logger.error(f"Error calculating warp matrix for {filename}: {e}")
        raise

def warp_coordinates(h5_file, logger):
    '''
    Apply affine transformation to the input HDF5 file to align with R2 camera orientation
    
    Return:
    a pandas DataFrame
    '''
    try:
        logger.info(f"Starting transformation for: {h5_file.split('/')[-1]}")

        df = h5_preprocessing(h5_file) 

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
        warp_matrix = get_warp_matrix(h5_file.split('/')[-1], logger)

        # Apply affine transformation to each pair of coordinates
        transformed_coords = np.empty_like(coords)
        for i in range(0, coords.shape[1], 2): 
            points = coords[:, i:i+2]
            points = points.reshape(-1, 1, 2)
            transformed_points = cv2.transform(points, warp_matrix).reshape(-1, 2)

            transformed_coords[:, i:i+2] = transformed_points

        # Update the dataframe with the transformed and cropped coordinates
        df[warped_columns] = transformed_coords
        
        logger.info(f"Transformation complete for file: {h5_file.split('/')[-1]}")
        return df

    except Exception as e:
        logger.error(f"Error processing {h5_file.split('/')[-1]}: {e}")
        raise   

