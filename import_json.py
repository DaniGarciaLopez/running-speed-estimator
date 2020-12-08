import os
import json
import numpy as np


def get_keypoints():

    poses=[]
    keypoints=[]

    # Get all json filenames from dir
    path_to_json = 'runner/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    for json_filename in json_files: #Iterate with all json filenames
        path=os.path.join(path_to_json, json_filename) #Create path to json file
        with open(path) as jsonFile: #Open json file
            jsonObject = json.load(jsonFile) #Create json object
            poses.append(jsonObject) #Append json object in poses
            jsonFile.close()

    #shutil.rmtree(path_to_json) #Remove json folder

    #Extract keypoints
    for pose in poses:
        keypoints.append(pose.get('people')[0].get('pose_keypoints_2d')) #Extract keypoints from skeleton and save it in keypoints array. Only works if number_people_max=1

    # Body part locations (x, y) and detection confidence (c) formatted as x0,y0,c0,x1,y1,c1,....

    kp = []

    # here we convert the (frames)*75 array into a (frames)*25*3
    for keypoint in keypoints:
        temp_kp = np.array(keypoint).reshape(25, 3)
        kp.append(temp_kp)

    return kp

def interpolate_uncertain_points(kp):

    #here were change the uncertain x and y values for the average of the previous and next point
    for frame in range (1,len(kp)-1):
        for kp_id in range (len(kp[frame])):
            if kp[frame][kp_id][2]<0.6:
                kp[frame][kp_id][0] = (kp[frame-1][kp_id][0]+kp[frame+1][kp_id][0])/2
                kp[frame][kp_id][1] = (kp[frame - 1][kp_id][1] + kp[frame + 1][kp_id][1]) / 2
                kp[frame][kp_id][2] = 1

    return kp
