from transform_coordinates import transform_coordinates
from smooth_data import smooth_data
from label_decision import label_decision
from label_trials import label_trials
from append_time_info import append_time_info
import os

video_folder = '/Users/yang/Documents/Wilbrecht_Lab/SLEAP_video'
filename = 'RRM030_Day139_R1_turns.avi.predictions_analysis.h5'
input_h5 = os.path.join(video_folder, filename)
columns_to_smooth = [
        'warped Head x', 'warped Head y',
        'warped Neck x', 'warped Neck y',
        'warped Torso x', 'warped Torso y',
        'warped Tailhead x', 'warped Tailhead y'
    ]

df = transform_coordinates(input_h5)
appended_df = append_time_info(df, video_folder, filename)

smoothed_df = smooth_data(appended_df, columns_to_smooth)

# label decisions
labeled_df = label_decision(smoothed_df)

labeled_t_df = label_trials(labeled_df)

labeled_t_df.to_csv('test_result.csv')