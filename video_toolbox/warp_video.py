import cv2
import numpy as np
import os
from rr_sleap_track.transform_coordinates import get_warp_matrix

input_path = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/RRM026_Day151_R1_turns.avi' # Update this with the path to your video
dirname, filename = os.path.split(input_path)
base, extension = os.path.splitext(filename)
output_image_path = os.path.join(dirname, base + '_warped_frame.jpg')

def extract_and_warp_frame(input_path, output_image_path, warp_matrix):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    
    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to read the frame from the video.")
        return
    
    # Apply the affine transformation
    height, width = (60, 90)
    transformed_frame = cv2.warpAffine(frame, warp_matrix, (width, height))
    
    # Save the transformed frame as an image
    cv2.imwrite(output_image_path, transformed_frame)
    
    # Release the video capture object
    cap.release()
    print(f"Transformed frame saved as {output_image_path}")

warp_matrix = get_warp_matrix(input_path.split('/')[-1], logger=None)
extract_and_warp_frame(input_path, output_image_path, warp_matrix)
