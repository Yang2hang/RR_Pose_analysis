from transform_coordinates import transform_coordinates
from smooth_data import smooth_data
from label_decision import label_decision
from label_trials import label_trials

input_h5 = '/Users/yang/Documents/Wilbrecht_Lab/SLEAP_Analysis/RRM030_camR1_Day134_Turns.avi.predictions.analysis.h5'
columns_to_smooth = [
        'warped Head x', 'warped Head y',
        'warped Neck x', 'warped Neck y',
        'warped Torso x', 'warped Torso y',
        'warped Tailhead x', 'warped Tailhead y'
    ]

df = transform_coordinates(input_h5)

smoothed_df = smooth_data(df, columns_to_smooth)

# label decisions
labeled_df = label_decision(smoothed_df)

labeled_t_df = label_trials(labeled_df)

print(labeled_df.head(50))