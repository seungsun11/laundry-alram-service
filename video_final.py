import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import time
import requests
from datetime import datetime
# 쓰고 있는 걸 1 , 사용 가능한 건 0


def getCurrentTime():
    return time.time()
def getDiffTimeToTime(dtTime) :
    return time.time() - dtTime

face_cascade = cv2.CascadeClassifier('cascade.xml') # 세탁기 LED에 초점 두기
face_cascade2 = cv2.CascadeClassifier('available.xml') # 사용가능한지 판별

video_capture = cv2.VideoCapture('laundry_.mp4') # 사용할 영상 이름 // '0' = 컴퓨터 전방 카메라
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

count1_1 = 0
count1_2 = 0
count2_1 = 0
count2_2 = 0
starttime = getCurrentTime()
time1 = starttime
time2 = starttime
available_count1 = 0
available_count2 = 0
running_count1 = 0
running_count2 = 0
reftime_1 = 0
reftime_2 = 0

print("%-20s%-20s%-20s"%("time","laundry1","laundry2"))
while True:
    ret, frame = video_capture.read()
    frame1 = frame[120:220,100:300] # [y, y+delta y , x: x + delta x]
    frame2 = frame[120:220,600:800]
    # [y:y+h, x : x+w] (base_1 : [100:250, 200: 500] base_2 : [80:230,950:1250]
    #laundry_ : [150:300, 100:400]
    # laundry1_1 : [200:350, 200:500] laundry1_2 : [200:350,1000:1300]
    # base2_1 : [150:300, 200:500] base2_2 = frame[180:270, 830:1170]
    # video1 : [200:350 , 600:900]
    # video2 : [200:350 , 600:900]
    # vidoe3 : [100:250, 1000:1300]
    # video4_available : [400:550, 800:1100]
    #video6 : [280:350, 200:360]
    frame1 = cv2.resize(frame1, (640, 320), interpolation=cv2.INTER_AREA)
    frame2 = cv2.resize(frame2, (640, 320), interpolation=cv2.INTER_AREA)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    faces1_1 = face_cascade.detectMultiScale(gray1, 1.2, 5) # gray, 1.6, 5
    faces2_1 = face_cascade.detectMultiScale(gray2, 1.2, 5) # gray, 1.6, 5

    for (x,y,w,h) in faces1_1:
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray1_1 = faces1_1[y:y+h, x:x+w]
        roi_color1_1 = faces1_1[y:y+h, x:x+w]
        faces1_2 = face_cascade2.detectMultiScale(frame1[y:y+h , x: x+w], 1.1, 1)
        count1_1 += 1


        for (x1, y1, w, h) in faces1_2:
            cv2.rectangle(frame1, (x1+x, y1+y), (x1+x + w, y1+y + h), (0, 255,0), 2)
            cv2.putText(frame1,"available",(x1+x,y1+y),cv2.FONT_ITALIC,2,(0,255,0),1,cv2.LINE_AA)
            roi_gray1_2 = faces1_2[y1+y:y1+y + h, x1+x:x1+x + w]
            roi_color1_2 = faces1_2[y1+y :y1+y + h, x1+x:x1+x + w]
            count1_2 += 1

    # frame2 is another fraction of same video and same time
    for (x,y,w,h) in faces2_1:
        cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray2_1 = faces2_1[y:y+h, x:x+w]
        roi_color2_1 = faces2_1[y:y+h, x:x+w]
        faces2_2 = face_cascade2.detectMultiScale(frame2[y:y+h , x: x+w], 1.1, 1)
        count2_1 += 1


        for (x2, y2, w, h) in faces2_2:
            cv2.rectangle(frame2, (x2+x, y2+y), (x2+x + w, y2+y + h), (0, 255,0), 2)
            cv2.putText(frame2,"available",(x2+x,y2+y),cv2.FONT_ITALIC,2,(0,255,0),1,cv2.LINE_AA)
            roi_gray = faces2_2[y2+y:y2+y + h, x2+x:x2+x + w]
            roi_color = faces2_2[y2+y :y2+y + h, x2+x:x2+x + w]
            count2_2 += 1

    deltatime1 = getDiffTimeToTime(time1)
    if int(deltatime1) >= 2:
        time1 = getCurrentTime()
        if count1_1 != 0 and count1_2/count1_1 >= 0.1:
            available_count1 += 1
        else:
            running_count1 += 1
        now = datetime.now()
        hour_min = str(now.hour) + ":" + str(now.minute)
        if running_count1 + available_count1 >= 5:
            print("%-20d" % getDiffTimeToTime(starttime), end='')
            if available_count1 >= 4:
                print("%-20s"%"Available",end = '')
                URL = 'http://192.168.112.168:3000/updateUser/laundry_1'
                response = requests.put(URL, data={"state": "0"})
                print(response.status_code)
                print(response.text)
            elif running_count1 >= 4:
                print("%-20s"%"Running", end = '')
                URL = 'http://192.168.112.168:3000/updateUser/laundry_1'
                if reftime_1 == 0 or getDiffTimeToTime(reftime_1)>3300:
                    response = requests.put(URL, data = {"state":"1","date":hour_min})
                    reftime_1 = getCurrentTime()
                print(response.status_code)
                print(response.text)
            else:
                print('%-20s'%"Can't know", end = '')
            available_count1, running_count1 = 0,0
        count1_1, count1_2 = 0, 0
    cv2.imshow('frame1', frame1)

    deltatime2 = getDiffTimeToTime(time2)
    if int(deltatime2) >= 2:
        time2 = getCurrentTime()
        if count2_1 != 0 and count2_2 / count2_1 >= 0.1:
            available_count2 += 1
        else:
            running_count2 += 1

        if running_count2 + available_count2 >= 5:
            if available_count2 >= 4:
                print("%-20s" % "Available")
                URL = 'http://192.168.112.168:3000/updateUser/laundry_2'
                response = requests.put(URL, data={"state": "0"})
                print(response.status_code)
                print(response.text)
            elif running_count2 >= 4:
                print("%-20s" % "Running")
                URL = 'http://192.168.112.168:3000/updateUser/laundry_2'
                if reftime_2 == 0 or getDiffTimeToTime(reftime_2) >= 3300:
                    response = requests.put(URL, data ={"state":"1","date":hour_min})
                    reftime_2 = getCurrentTime()
                # response = requests.put(URL, data={"state": "1"})
                print(response.status_code)
                print(response.text)
            else:
                print("%-20s" % "Can't know")
            available_count2, running_count2 = 0, 0
        count2_1, count2_2 = 0, 0


    cv2.imshow('frame2',frame2)
    cv2.imshow('full frame',cv2.resize(frame, (640, 320), interpolation=cv2.INTER_AREA))

    cv2.waitKey(1)
cv2.destroyAllWindows()



