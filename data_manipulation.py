#Requires Matplotlib, numpy and scipy for python

import scipy.signal
import import_json as ij
import numpy as np
import matplotlib.pyplot as plt

kp = ij.get_keypoints()     #kp is a list of all the 25x3 lists of keypoints
#kp = ij.interpolate_uncertain_points(kp)       #uncomment to interpolate uncertain points

#constants
eyes=17
neck=1
hip=8
left_knee=13
right_knee=10
left_ankle=14
right_ankle=11

x_values = []
y_values = []

#imports a series of keypoints and outputs smoothed data
def smooth_data(kp):
    kp_filtered = kp
    for kp_id in range(25):
        x_values.clear()
        y_values.clear()
        for f_kp in kp:
            x_values.append(f_kp[kp_id][0])
            y_values.append(f_kp[kp_id][1])
        x_values_filtered = scipy.signal.savgol_filter(x_values, 15, 2)
        y_values_filtered = scipy.signal.savgol_filter(y_values, 15, 2)
        for i in range(len(kp)):
            kp_filtered[i][kp_id][0]=x_values_filtered[i]
            kp_filtered[i][kp_id][1]=y_values_filtered[i]
    return kp_filtered
