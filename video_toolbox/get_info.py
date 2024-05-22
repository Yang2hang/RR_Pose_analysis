import cv2

def get_video_info(filepath):
    cap = cv2.VideoCapture(filepath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    
    print(f"Resolution: {width}x{height}")
    print(f"Duration: {duration} seconds")
    print(f"Frames per second: {fps}")

    cap.release()

# Replace 'path_to_video.avi' with the path to your video file
get_video_info('RRM030_camR1_Day134_Turns.avi')
