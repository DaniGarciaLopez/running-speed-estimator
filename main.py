import cv2
import import_json as ij
import numpy as np
import math
from matplotlib import pyplot as plt

#key data
athlete_height = 180 # in cm
camera_fps = 60

#importing json file
keypoints = ij.get_keypoints()
kp = []

#init
speed = 0
max_distance = 0
stride_frames = 0
prev_ankle_distance = 0

#constants
bottom_left_of_screen = (20, 700)
eyes=17
neck=1
hip=8
left_knee=13
right_knee=10
left_ankle=14
right_ankle=11

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang

def get_pixels_per_meter(kp):   #returns how many pixels correlate to 1 meter in the frame
    coord_eyes = (kp[eyes][0], kp[eyes][1])
    coord_neck = (kp[neck][0], kp[neck][1])
    coord_hip = (kp[hip][0], kp[hip][1])
    coord_knee = (kp[left_knee][0], kp[left_knee][1])
    coord_ankle = (kp[left_ankle][0], kp[left_ankle][1])
    distance = 0        #we add the distance between keypoints 16 1 8 13 14
    distance += math.dist(coord_eyes,coord_neck)
    distance += math.dist(coord_neck, coord_hip)
    distance += math.dist(coord_hip, coord_knee)
    distance += math.dist(coord_knee, coord_ankle)

    pixels = int(distance/athlete_height*100)
    return pixels

def draw_meter_lines(frame, kp):
    values = []
    ppm = get_pixels_per_meter(kp)
    for keypoint in kp:      #we get just the y values
        values.append(keypoint[1])
    max_value = int(max(values))    #we draw the line at the lowest keypoint (approx the floor)
    frame = cv2.line(frame, (0, max_value), (1280, max_value), (255, 255, 255), 2)
    for meter in range(int(1280/ppm)+1):
        frame = cv2.line(frame, (0+(ppm*meter), max_value), (0+(ppm*meter), max_value+10), (255, 255, 255), 3)
        frame = cv2.putText(frame, str(meter), (-10+(ppm*meter), 44 + max_value),cv2.FONT_HERSHEY_SIMPLEX,       # font
                    1,      #font scale
                    (255, 255, 255),   #   font color
                    2)
    return frame

def draw_keypoints(frame, kp):  #kp must be in 25*3 format
    kpid = 0
    for point in kp:  # drawing a circle for each kp
        center = (int(point[0]), int(point[1]))
        center_high = ((int(point[0])-5, int(point[1])-15))      #used for writing its id
        frame = cv2.circle(frame, center, 10, (0, int(255 * point[2]), 255 * (1 - point[2])), 3)       #draws green cirle if certain, red if not
        cv2.putText(frame,
                    str(kpid),
                    center_high,
                    cv2.FONT_HERSHEY_SIMPLEX,  # font
                    0.5,  # font scale
                    (255, 255, 255),  # font color
                    1)  # line type
        kpid += 1
    return frame

#main
while(1):
    cap = cv2.VideoCapture('makau.mp4')
    total_frame_count = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        kp = keypoints[total_frame_count]

        frame = draw_keypoints(frame, kp)

        hip_coord = (kp[hip][0], kp[hip][1])
        left_ankle_coord = (kp[left_ankle][0], kp[left_ankle][1])
        right_ankle_coord = (kp[right_ankle][0], kp[right_ankle][1])
        ankle_distance = math.fabs(left_ankle_coord[0]-right_ankle_coord[0])
        if ankle_distance > prev_ankle_distance-5:
            stride_frames +=1
            prev_ankle_distance = ankle_distance
        else:
            stride_pixels = ankle_distance
            stride_meters = stride_pixels/get_pixels_per_meter(kp)
            stride_time = stride_frames*(1/camera_fps)
            try:
                speed = (stride_meters/stride_time)*3.6
            except ZeroDivisionError:
                print ("Division by zero")
            stride_frames=0
            prev_ankle_distance = ankle_distance
            print("The stride has " + str(stride_meters) + " meters")
            print("The stride spent " + str(stride_time) + " seconds")
            print("The speed is " + str(speed) + " kilometers per hour")


        cv2.putText(frame,
                    str(round(speed,2))+' Km/h',
                    bottom_left_of_screen,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2,
                    (255,255,255),
                    2)


        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()
        total_frame_count += 1

cap.release()
cv2.destroyAllWindows()

