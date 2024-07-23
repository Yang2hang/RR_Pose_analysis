file_path = '/Users/yang/Documents/Wilbrecht_Lab/code/RR_Pose_analysis/video_toolbox/bonsai_roi.txt'
with open(file_path, 'r') as f:
    all_pts = []
    for line in f.readlines():
        p1, p2 = line.split(',Point')[1:3]
        all_pts.append(eval(p1))
        all_pts.append(eval(p2))