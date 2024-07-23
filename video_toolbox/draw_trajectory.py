# Assuming CV is an alias for the OpenCV module and all necessary imports are done
import cv2 as CV

# Define colors and thickness
Hallcolor = (0, 255, 0)  # g
Offercolor = (0, 0, 255)  # r
Acceptcolor = (255, 0, 0)  # b
thickness = 2  # Example thickness
image_height = 240

def draw_trajectory(trajectory):
    # R4
    # Draw Hall 1
    CV.line(trajectory, (341//2, 228//2), (420//2, 228//2), Hallcolor, thickness)
    # Draw offer zone 4
    CV.line(trajectory, (426//2, 155//2), (426//2, 188//2), Offercolor, thickness)
    # Draw reward zone 4
    CV.line(trajectory, (419//2, 182//2), (371//2, 182//2), Acceptcolor, thickness)
    CV.line(trajectory, (371//2, 182//2), (339//2, 182//2), Acceptcolor, thickness)




thresholds_file = '/Users/yang/Documents/Wilbrecht_Lab/code/RR_Pose_analysis/video_toolbox/decision_thresholds.txt'
photos_dir = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video'
output_dir = '/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video'
trajectory = CV.imread('/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/R3.png')
draw_trajectory(trajectory)
CV.imwrite('/Users/yang/Documents/Wilbrecht_Lab/data/sleap_video/R3_w_threshold.png', trajectory)