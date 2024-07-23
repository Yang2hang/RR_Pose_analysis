import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

def extract_first_frame(video_path, save_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not read the first frame from {video_path}")
    save_filename = os.path.join(save_path, f"R{frame_number}.png")
    cv2.imwrite(save_filename, frame)
    return frame
    

# Paths to the video files
video_paths = [
    "/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/RRM026_Day151_R1_turns.avi", 
    "/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/RRM026_Day151_R2_turns.avi", 
    "/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/RRM026_Day151_R3_turns.avi", 
    "/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/RRM026_Day151_R4_turns.avi", 
]
save_path = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video'

# Extract the first frame from each video and save it
frames = []
for i, video_path in enumerate(video_paths):
    frame = extract_first_frame(video_path, save_path, frame_number=i+1)
    frames.append(frame)
