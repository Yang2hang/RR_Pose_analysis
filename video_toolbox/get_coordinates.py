import cv2
import matplotlib.pyplot as plt
import os

folder_path = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video'
video = 'RRM026_Day151_R4_turns.avi'# enter your video path here
video_path = os.path.join(folder_path, video)

def show_frame(video_path, frame_number=0):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Move to the frame_number
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to get the frame.")
        cap.release()
        return

    # Convert the frame to RGB (matplotlib expects RGB images)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame
    plt.figure(figsize=(10, 8))
    plt.imshow(frame_rgb)
    plt.axis('on')  # Turn on axis to see the pixel coordinates in the toolbar
    plt.title(f"Frame {frame_number}")
    plt.show()

    # Release the video capture object
    cap.release()

# Path to your video
show_frame(video_path, frame_number=300)
