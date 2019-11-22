import time
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


# Variables
_url = 'https://westus2.api.cognitive.microsoft.com/face/v1.0/detect'
_key = 'bc027dc227484433a77d7b613807d230' #Here you have to paste your primary key
_maxNumRetries = 10
cap = cv2.VideoCapture('emotion_video/Anger_1.mp4')
timeF = 60
c=1
sec = 0

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video  file")

# Read until video is completed
while(cap.isOpened()):
    ret, frame = cap.read()
    if (ret == True):
        if(c%timeF == 0):
            #cv2.imshow('image', frame)
            type = "angry"
            video_id = "015"

            cv2.imwrite("frame1.jpg", frame)
            pathToFileInDisk = r'frame1.jpg'
            sec+=1
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
            result = processRequest( json, data, headers, params, _url )
            
            # /// build data ///
            # if result == []:
            #     no face
            if result == []:
                continue
            firstface_dic = result[0]
            faceAttributes_dic = firstface_dic['faceAttributes']
            #print(faceAttributes_dic)
            time = sec
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
