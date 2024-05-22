import cv2
import math
import os

input_path = 'RRM030_camR2_Day134_Turns_rotated.avi' # Update this with the path to your video
base, extension = os.path.splitext(input_path)
output_path = base + '_cropped' + extension

def crop_video(input_path, output_path, camera):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    width, height = (176, 145)
    
    crop_dims = { # set the default crop parameters for each camera (top left corner of the cropping region)
        'R1': (64, 81),
        'R2': (88, 0),
        'R3': (48, 50),
        'R4': (107, 13)
    }
    x, y = crop_dims[camera]
    
    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Crop the frame
        cropped_frame = frame[y:y+height, x:x+width]
        
        # Write the cropped frame
        out.write(cropped_frame)
    
    # Release everything when job is finished
    cap.release()
    out.release()

if 'R1' in input_path:
    camera = 'R1'
elif 'R2' in input_path:
    camera = 'R2'
elif 'R3' in input_path:
    camera = 'R3'
elif 'R4' in input_path:
    camera = 'R4'
else:
    print('cannot identify camera')

crop_video(input_path, output_path, camera)
