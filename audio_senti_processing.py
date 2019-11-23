import subprocess
import os

def call_convert_video_to_audio(video_name):
    command = "ffmpeg -i emotion_video/" + video_name + ".mp4  -ab 160k -ac 2 -ar 44100 -vn emotion_audio/" + video_name + ".wav"
    subprocess.call(command, shell=True)

def convert_video_to_audio():
    files = os.listdir('emotion_video/')
    for one_file in files:
        if one_file[-3:] != 'mp4':
            continue
        video_name = one_file[:-4]
        print(video_name)
        call_convert_video_to_audio(video_name)
        

