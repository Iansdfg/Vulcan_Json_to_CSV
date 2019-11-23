import time
import os
import csv
import requests
import cv2
import operator
import numpy as np
import matplotlib.pyplot as plt
import pylab
import imageio
import skimage.io
import math
from process_image import processRequest
from process_image import renderResultOnImage
from CRUD_m import create_data
from CRUD_m import read_data
from CRUD_m import close_connection
from CRUD_m import get_connection

# Import library to display results
import matplotlib.pyplot as plt
# Display images within Jupyter

def get_fame(video_name):
    video = cv2.VideoCapture(video_name)
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)) 
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)) 
    video.release(); 
    return fps


def get_single_file_data(filename, res):
    video_frame = get_fame('emotion_video/' + filename ) 
    # Variables
    cap = cv2.VideoCapture('emotion_video/' + filename)
    _url = 'https://westus2.api.cognitive.microsoft.com/face/v1.0/detect'
    _key = 'bc027dc227484433a77d7b613807d230' #Here you have to paste your primary key
    _maxNumRetries = 10
    timeF = video_frame
    print("timeF: ", timeF)
    c=1
    sec = 0


    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video  file")

    # Read until video is completed
    while(cap.isOpened()):
        ret, frame = cap.read()
        # print('ret: ', ret, 'frame: ', frame.shape)
        if (ret == True):
            # print(c, sec, c%timeF)
            if(int(c%timeF) == 0):
                #cv2.imshow('image', frame)

                video_id = filename[:-4]
                type = 'None'
                if 'Anger' in filename or 'annoy' in filename:
                    type = "angry"
                elif 'joy' in filename:
                    type = "happy"
                elif 'sad' in filename:
                    type = "sad"

                cv2.imwrite("frame1.jpg", frame)
                pathToFileInDisk = r'frame1.jpg'
                sec += 1
                with open( pathToFileInDisk, 'rb' ) as f:
                    data = f.read()
                headers = dict()
                headers['Ocp-Apim-Subscription-Key'] = _key
                headers['Content-Type'] = 'application/octet-stream'

                json = None
                params = {
                    #'returnFaceId': 'true',
                    #'returnFaceLandmarks': 'false',
                    'returnFaceAttributes': 'age,gender,smile,emotion',
                    #'returnFaceAttributes': 'emotion',
                }
                path = "frame1.jpg"
                result = processRequest(json, data, headers, params, _url )
        
                time = sec
                # /// build data ///
                # if result == []:
                #     no face
                if result == []:
                    data =  {
                            'video_id': video_id, 
                            'smile': 0, 
                            'gender':0, 
                            'anger': 0, 
                            'contempt':0, 
                            'disgust':0, 
                            'fear':0, 
                            'happiness':0, 
                            'neutral':0, 
                            'sadness':0, 
                            'surprise':0, 
                            'time':time, 
                            'type':type 
                            }
                else: 
                    firstface_dic = result[0]
                    faceAttributes_dic = firstface_dic['faceAttributes']
                    #interval = math.ceil(sec/10)
                    smile = faceAttributes_dic['smile']
                    gender = faceAttributes_dic['gender']
                    #age = faceAttributes_dic['age']
                    anger = faceAttributes_dic['emotion']['anger']
                    contempt = faceAttributes_dic['emotion']['contempt']
                    disgust = faceAttributes_dic['emotion']['disgust']
                    fear = faceAttributes_dic['emotion']['fear']
                    happiness = faceAttributes_dic['emotion']['happiness']
                    neutral = faceAttributes_dic['emotion']['neutral']
                    sadness = faceAttributes_dic['emotion']['sadness']
                    surprise = faceAttributes_dic['emotion']['surprise']
                    data =  {
                            'video_id': video_id, 
                            'smile': smile, 
                            'gender':gender, 
                            'anger': anger, 
                            'contempt':contempt, 
                            'disgust':disgust, 
                            'fear':fear, 
                            'happiness':happiness, 
                            'neutral':neutral, 
                            'sadness':sadness, 
                            'surprise':surprise, 
                            'time':time, 
                            'type':type 
                            }
                print(data)
                res.append(data)
        

                # /// upload to database ///
                # connection = get_connection()
                #table_name = 'facial_emotion_dataset'
                #create_data(table_name, data, connection)

                k = cv2.waitKey(2)
                #/// q键退出 ///
                if (k & 0xff == ord('q')):
                    break
            c+=1
        else:
            break

    # close_connection(connection)
    print(c)
    print(sec)
    cap.release()
    cv2.destroyAllWindows()


def write_array_to_CSV(arrary, filename):
    with open(filename, mode='w') as csv_file:
        fieldnames = [
            'video_id', 
            'smile', 
            'gender', 
            'anger', 
            'contempt', 
            'disgust', 
            'fear', 
            'happiness', 
            'neutral', 
            'sadness', 
            'surprise', 
            'time', 
            'type', 
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in arrary:
            writer.writerow(
                {
                    'video_id': row['video_id'], 
                    'smile': row['smile'], 
                    'gender':row['gender'], 
                    'anger': row['anger'], 
                    'contempt':row['contempt'], 
                    'disgust':row['disgust'], 
                    'fear':row['fear'], 
                    'happiness':row['happiness'], 
                    'neutral':row['neutral'],
                    'sadness':row['sadness'],
                    'surprise':row['surprise'], 
                    'time':row['time'],
                    'type':row['type'],  
                }
            )

if __name__ == "__main__":
    res = []
    files = os.listdir('emotion_video/')
    for one_file in files:
        if one_file[-3:] != 'mp4':
            continue
        get_single_file_data(one_file, res)
    write_array_to_CSV(res, 'test_1.csv')


    # res = []
    # get_single_file_data('joy_8.mp4', res)
    # # for ele in res:
    # #     print(ele)
