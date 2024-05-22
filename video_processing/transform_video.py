import cv2
import numpy as np
import os

def get_warp_matrix(filename):
    '''
    define warp matrix by the key points coordinates according to different cameras
    3 key points are 3 corners of the restaurants
    '''
    if 'R1' in filename:
        srcTri = np.array([[186.9, 178.3], [226, 178.3], [224, 137.6]]).astype(np.float32)
    elif 'R2' in filename:
        srcTri = np.array([[271.2, 128.3], [270.8, 95.6], [228.7, 95.3]]).astype(np.float32)
    elif 'R3' in filename:
        srcTri = np.array([[208.5, 53.5], [170, 54.5], [170.7, 89.5]]).astype(np.float32)
    elif 'R4' in filename:
        srcTri = np.array([[108.4, 119.3], [109.1, 158.5], [155.3, 159.2]]).astype(np.float32)
    else:
        print('Cannot identify camera for', filename)
        return None

    dstTri = np.array([[166, 46], [166, 10], [125, 10]]).astype(np.float32)
    warp_matrix = cv2.getAffineTransform(srcTri, dstTri)
    return warp_matrix

def transform_video(video_folder):
    '''
    transform the video according to the warp matrix
    '''
    for filename in os.listdir(video_folder):
        if filename.endswith('.avi'):
            input_video = os.path.join(video_folder, filename)
            base, extension = os.path.splitext(input_video)
            output_video = base + '_warped' + extension
            
            warp_matrix = get_warp_matrix(filename)
            # Open the input video
            cap = cv2.VideoCapture(input_video)
            fps = cap.get(cv2.CAP_PROP_FPS)
            width, height = (176, 145)

            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
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
        
        
    