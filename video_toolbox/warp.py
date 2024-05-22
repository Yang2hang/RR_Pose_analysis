import cv2
import numpy as np
import os

input_path = 'RRM030_camR4_Day134_Turns.avi' # Update this with the path to your video
base, extension = os.path.splitext(input_path)
output_path = base + '_warped' + extension

def transform_video(input_path, output_path, warp_matrix):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = (176, 145)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Apply the affine transformation
        transformed_frame = cv2.warpAffine(frame, warp_matrix, (width, height))
        
        # Write the transformed frame to the output video
        out.write(transformed_frame)
    
    # Release everything when the job is finished
    cap.release()
    out.release()

if 'R1' in input_path:
    srcTri = np.array( [[186.9, 178.3], [226, 178.3], [224, 137.6]] ).astype(np.float32)
elif 'R2' in input_path:
    srcTri = np.array( [[271.2, 128.3], [270.8, 95.6], [228.7, 95.3]] ).astype(np.float32)
elif 'R3' in input_path:
    srcTri = np.array( [[208.5, 53.5], [170, 54.5], [170.7, 89.5]] ).astype(np.float32)
elif 'R4' in input_path:
    srcTri = np.array( [[108.4, 119.3], [109.1, 158.5], [155.3, 159.2]] ).astype(np.float32)
else:
    print('cannot identify camera')

dstTri = np.array( [[166, 46], [166, 10], [125, 10]] ).astype(np.float32)
warp_mat = cv2.getAffineTransform(srcTri, dstTri)

transform_video(input_path, output_path, warp_mat)
