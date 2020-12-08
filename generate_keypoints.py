# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time

import os, json
import pandas as pd
import shutil
import matplotlib.pyplot as plt

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('/usr/local/python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    path_to_video='runner.mp4'
    parser = argparse.ArgumentParser()
    #parser.add_argument('--input', type=str, default='video')
    #parser.add_argument('--video', type=str, default=path_to_video)
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "models/"


    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython(op.ThreadManagerMode.Synchronous)
    opWrapper.configure(params)
    opWrapper.execute()

    poses=[]
    keypoints=[]
    # Get all json filenames from dir
    path_to_json = '1/'
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


    print("Json files generated in folder: ", path_to_json)
    
except Exception as e:
    print(e)
    sys.exit(-1)
