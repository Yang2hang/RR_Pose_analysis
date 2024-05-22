import ffmpeg
import math
import cv2
import os

input_path = 'RRM030_camR3_Day134_Turns.avi' # Update this with the path to your video
base, extension = os.path.splitext(input_path)
output_path = base + '_rotated' + extension

def rotate_video(input_path, output_path, camera):
    # Open the video
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    # Original dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Adjust output dimensions and rotation function based on the angle
    if camera == 'R1':
        rotated_func = cv2.ROTATE_90_CLOCKWISE
        new_width, new_height = height, width
    elif camera == 'R2':
        rotated_func = cv2.ROTATE_180
        new_width, new_height = width, height
    elif camera == 'R3':
        rotated_func = cv2.ROTATE_90_COUNTERCLOCKWISE
        new_width, new_height = height, width

    out = cv2.VideoWriter(output_path, fourcc, 30.0, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Rotate the frame
        rotated_frame = cv2.rotate(frame, rotated_func)
        
        # Write the rotated frame to the output video
        out.write(rotated_frame)

    # Release resources
    cap.release()
    out.release()

if 'R1' in input_path:
    camera = 'R1'
elif 'R2' in input_path:
    camera = 'R2'
elif 'R3' in input_path:
    camera = 'R3'
else:
    print('cannot identify camera')

rotate_video(input_path, output_path, camera)