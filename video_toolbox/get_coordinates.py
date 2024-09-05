import cv2
import matplotlib.pyplot as plt
import os
import imageio


photo_path = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/R4_w_threshold.png'

def show_frame(photo_path):
    # Read the image
    image = imageio.imread(photo_path)
    
    # Display the frame
    title = os.path.split(photo_path)[-1]
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis('on')  # Turn on axis to see the pixel coordinates in the toolbar
    plt.title(f"{title}")
    plt.show()

# Show the frame
show_frame(photo_path)
