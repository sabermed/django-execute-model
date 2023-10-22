import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import os

model=YOLO('videos/utils/yolov8s.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)



cap=cv2.VideoCapture('videos/utils/test3.mp4') #add  loop to automaticlly get the videos path within given folder


my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count=0
tracker=Tracker()

s=0
area_c=set()

def imgwrite(img):

    filename = str(s)+'.png'


    cv2.imwrite(os.path.join(r"media/UntitledFolder",filename), img) # add the destination folder path
while True:
    ret,frame = cap.read()
    if not ret:

        break
    count += 1
    if count % 2 != 0:
        continue


    #frame=cv2.resize(frame,(1020,500))

    results=model.predict(frame)

    a=results[0].boxes.boxes

    px=pd.DataFrame(a).astype("float")

    list=[]
    for index,row in px.iterrows():


        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'person' in c:
            list.append([x1,y1,x2,y2])

    bbox_idx=tracker.update(list)
    for bbox in bbox_idx:
        x3,y3,x4,y4,id=bbox

        cv2.rectangle(frame,(x3,y3),(x4,y4),(0,255,0),2)
        cv2.circle(frame,(x4,y4),4,(255,0,255),-1)
        cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)

        crop=frame[y3:y4,x3:x4]
        s +=1

        imgwrite(crop) # delete

    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()