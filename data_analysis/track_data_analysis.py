import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d
import os
from scipy.interpolate import interp1d
from h5_preprocessing import h5_preprocessing

file_path = '/home/wholebrain/sleap_models/20240402_RR_n24/Videos'

combined_df_list = []
for filename in os.listdir(file_path):
    if filename.endswith('analysis.h5'):
        input_hdf = os.path.join(file_path, filename)
        df = h5_preprocessing(input_hdf)
        combined_df_list.append(df)
        print(f"Processed and cleaned {filename}")

combined_df = pd.concat(combined_df_list, ignore_index=True)

analysis_raw = pd.read_csv('analysis_raw.csv')
analysis = delete_missing_rows(analysis_raw)
total_frames = analysis.shape[0]
analysis.head()

sns.lineplot(data=analysis, x=analysis.index, y='Head yCoordinates')
plt.title('Head Y-Coordinate Over Time')
plt.xlabel('Frames')
plt.ylabel('Head Y-Coordinate')
plt.ylim(170, 10)
#plt.xlim(0, 46)
plt.grid(True)
plt.show()

# edge length standard deviation
frame_rate = 30  # frames per second

head_neck_len = np.sqrt(
    (analysis['Head xCoordinates'] - analysis['Neck xCoordinates'])**2 +
    (analysis['Head yCoordinates'] - analysis['Neck yCoordinates'])**2
)
neck_torso_len = np.sqrt(
    (analysis['Neck xCoordinates'] - analysis['Torso xCoordinates'])**2 +
    (analysis['Neck yCoordinates'] - analysis['Torso yCoordinates'])**2
)

torso_tailhead_len = np.sqrt(
    (analysis['Torso xCoordinates'] - analysis['Tailhead xCoordinates'])**2 +
    (analysis['Torso yCoordinates'] - analysis['Tailhead yCoordinates'])**2
)
head_neck_len_sd = np.std(head_neck_len)
neck_torso_len_sd = np.std(neck_torso_len)
torso_tailhead_len_sd = np.std(torso_tailhead_len)
print(
    f' head_neck_len_sd: {head_neck_len_sd}\n',
    f'neck_torso_len_sd: {neck_torso_len_sd}\n',
    f'torso_tailhead_len_sd: {torso_tailhead_len_sd}'
    )


# Calculate the angle of the neck-torso edge relative to the berticle axis for each frame
neck_torso_orientation = np.degrees(np.arctan2(
    analysis['Neck xCoordinates'] - analysis['Torso xCoordinates'],
    -(analysis['Neck yCoordinates'] - analysis['Torso yCoordinates'])
))

# Plotting the direction of neck-torso edge over time
plt.figure(figsize=(10, 6))
plt.plot(neck_torso_orientation, label='Neck-Torso Orientation')
plt.xlabel('Frames')
plt.ylabel('Angle')
plt.title('Neck-Torso Orientation Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Calculate the angle of the neck-tailhead edge relative to the verticle axis for each frame
neck_tailhead_orientation = np.degrees(np.arctan2(
    analysis['Tailhead xCoordinates'] - analysis['Neck xCoordinates'],
    analysis['Neck yCoordinates'] - analysis['Tailhead yCoordinates']
))

# Plotting the direction of neck-tailhead edge over time
plt.figure(figsize=(10, 6))
plt.plot(neck_tailhead_orientation[:47], label='Neck-Tailhead Orientation')
plt.xlabel('Frames')
plt.ylabel('Angle')
plt.title('Neck-Tailhead Orientation Over Time')
plt.legend()
plt.grid(True)
plt.show()

straight_walking = pd.DataFrame()
straight_walking_head_x = pd.DataFrame()

seg_num = 0
start_index = None
in_segment = False

for index, row in analysis.iterrows():
    if in_segment:
        if row['Head yCoordinates'] >= 123: # straight walk end (T-entry)
            seg_num+=1
            #segment_head_x = analysis.loc[index - 12:index, 'Head xCoordinates'].reset_index(drop=True)
            #straight_walking_head_x[f'Track {seg_num}'] = segment_head_x
            segment = analysis.loc[start_index:index]
            straight_walking = pd.concat([straight_walking, segment])
            in_segment = False
            start_index = None
    else:
        if row['Head yCoordinates'] < 80: # straight walk start
            start_index = index
            in_segment = True
if in_segment:
    segment = analysis.loc[start_index:]
    straight_walking = pd.concat([straight_walking, segment])

straight_walking.reset_index(drop=True, inplace=True)
straight_walking.head()
#print(f'Straight walking head x coordinates sd: {straight_walking_head_x.std(axis=0).mean()}')

"""Head angle is defined by the angle between head-neck vector and the trunk orientation (right = positive; left = negative). During the straight walking movement, the head angle should be stable. Rapid changes in head orientation are mostly due to recognition jitters, so we can use the standard deviation of head angle to represent model preformance."""

straight_trunk_orientation = np.degrees(np.arctan2(
    straight_walking['Neck xCoordinates'] - straight_walking['Torso xCoordinates'],
    -(straight_walking['Neck yCoordinates'] - straight_walking['Torso yCoordinates'])
))

straight_head_neck_orientation = np.degrees(np.arctan2(
    straight_walking['Head xCoordinates'] - straight_walking['Neck xCoordinates'],
    -(straight_walking['Head yCoordinates'] - straight_walking['Neck yCoordinates'])
))

straight_head_angle = straight_head_neck_orientation - straight_trunk_orientation

print(f'Head angle standard deviation = {np.std(straight_head_angle)}')

plt.figure(figsize=(10, 6))
plt.plot(straight_head_angle, label='Head Angle')
plt.xlabel('Frames')
plt.ylabel('Angle')
plt.title('Head Angle over time')
plt.legend()
plt.grid(True)
plt.show()

trunk_orientation_head = np.degrees(np.arctan2(
    analysis['Neck xCoordinates'] - analysis['Torso xCoordinates'],
    -(analysis['Neck yCoordinates'] - analysis['Torso yCoordinates'])
))

head_neck_orientation = np.degrees(np.arctan2(
    analysis['Head xCoordinates'] - analysis['Neck xCoordinates'],
    -(analysis['Head yCoordinates'] - analysis['Neck yCoordinates'])
))

trunk_orientation_tail = np.degrees(np.arctan2(
    analysis['Torso xCoordinates'] - analysis['Neck xCoordinates'],
    -(analysis['Neck yCoordinates'] - analysis['Torso yCoordinates'])
))

torso_tailhead_orientation = np.degrees(np.arctan2(
    analysis['Torso xCoordinates'] - analysis['Tailhead xCoordinates'],
    -(analysis['Torso yCoordinates'] - analysis['Tailhead yCoordinates'])
))

theta_1 = head_neck_orientation - trunk_orientation_head
theta_2 = torso_tailhead_orientation - trunk_orientation_tail

x = abs(theta_1+theta_2) / 2
y = (abs(theta_1) + abs(theta_2)) / 2

plt.scatter(x, y, s=5)
plt.grid(True)
plt.xlabel('abs of Mean')
plt.ylabel('Mean of abs')

#manual decision boundary
slope = 1
intercept = 6

x_values = np.linspace(x.min(), x.max(), 100)

y_values = slope * x_values + intercept

plt.plot(x_values, y_values, 'r')

plt.show()

num_points_above = np.sum(y > slope * x + intercept)

print(f'Proportion of twist-body frames is {num_points_above / total_frames}')

mask_positive_theta1_negative_theta2 = (theta_1 > 0) & (theta_2 < 0)

mask_negative_theta1_positive_theta2 = (theta_1 < 0) & (theta_2 > 0)

mask_heteroscedastic = mask_positive_theta1_negative_theta2 | mask_negative_theta1_positive_theta2

number_of_heteroscedastic_frames = np.sum(mask_heteroscedastic)

print(f'The number of frames are {number_of_heteroscedastic_frames}')

print(
    f'head_neck_len_sd: {head_neck_len_sd}\n'
    f'neck_torso_len_sd: {neck_torso_len_sd}\n'
    f'torso_tailhead_len_sd: {torso_tailhead_len_sd}\n'
    f'head angle standard deviation = {np.std(straight_head_angle)}\n'
    f'The number of frames are {number_of_heteroscedastic_frames}\n'
    f'Proportion of twist-body frames is {num_points_above / total_frames}\n'
    )

