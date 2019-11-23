# tmp_speech2text.py: 
# conver all audio into CSV files eg: 001_S_T.wav.csv 
import azure.cognitiveservices.speech as speechsdk
from speech_func import speech_recognize_continuous_from_file
from msrest.authentication import CognitiveServicesCredentials
from sentiment_functions import get_sentiment_score
import time
import wave
import math
import csv
import json
import os
from os import listdir
import statistics
speech_key, service_region = "d122e91d2df24ce889a13695542564c2", "eastus"
sentiment_key = 'f56de4b340b6472f951a0b5b7cfc8f8c'

def read_wirte_sigle_file(filename, id_number):
    current_path = './'
    read_folder_name = 'audio/'
    read_file = read_folder_name + filename
    if not '%s.json' %read_file in os.listdir(current_path):
        result,sentence_length = speech_recognize_continuous_from_file(read_file)
        result.append(sentence_length)
        with open('%s.json' % read_file,'w') as json_f:
            json.dump(result,json_f)
            result.pop()
    else:
        with open('%s.json' % read_file,'r') as json_f:
            result = json.load(json_f)
            sentence_length = result.pop()


    res = get_sentiment_score(result, sentiment_key, sentence_length)
    print(res)


    write_folder = 'CSV/'
    write_file = write_folder+filename
    with open(write_file + ".csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 
                        # 'duration', 
                        'id',
                        'score', 
                        'max', 
                        'min', 
                        'avg', 
                        'std', 
                        'sentense'])
        for data in res:
            writer.writerow([
                            math.ceil(data['Time']), 
                            # data['Duration'], 
                            id_number,
                            data['Sentiment Score'], 
                            data['max_score'],
                            data['min_score'],
                            data['avg_score'],
                            data['std_score'],
                            data['Sentence'],
                            ])
    
if __name__ == "__main__":

    # filename = '015_A_E.wav'
    # # id_number = filename[:3]
    # read_wirte_sigle_file(filename, 1)

    lists = os.listdir('emotion_audio/')
    for listt in lists:
        if listt[-3:] == 'wav':
            id_number = listt[:-1]
            read_wirte_sigle_file(listt, id_number)


