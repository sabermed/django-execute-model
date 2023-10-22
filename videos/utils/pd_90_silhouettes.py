from ultralytics import YOLO
import cv2
import numpy as np
model=YOLO('videos/utils/yolov8s.pt')

import cv2
import pandas as pd
import glob
import numpy as np
from ultralytics import YOLO
import datetime
import os
import shutil
def imgwrite(img,dest_path):
  filename = str(s)+'.jpg'
  cv2.imwrite(os.path.join(dest_path,filename), img) # add the destination folder path

my_file = open("videos/utils/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
###################################################################
######### loop over all png images of 180 degrée files########
folder_path = 'videos/utils/PD-90-Crops'
for file_name in os.listdir(folder_path):
  file_path = os.path.join(folder_path, file_name)
  s=0
  dest_path0=(file_name.split('-')[0]+'-'+file_name.split('-')[1]+'-'+file_name.split('-')[2]+'-'+file_name.split('-')[3]+'-silhouet')
  dest_path=('videos/utils/PD-90-Silhouet'+"/"+dest_path0)
  if not os.path.exists(dest_path):
    # Create a new empty folder
    os.makedirs(dest_path, exist_ok=True)
    for file_name1 in os.listdir(file_path):
      file_path1 = os.path.join(file_path,file_name1)
      predicted=model.predict(file_path1,save=True,save_txt=True)
      a=predicted[0].boxes.boxes
      px=pd.DataFrame(a).astype("float")
      list=[]
      for index,row in px.iterrows():
        d=int(row[5])
        c=class_list[d]
        if 'person' in c:
          invert=cv2.bitwise_not((predicted[0].masks.masks[0].numpy()).astype("uint8")*255)
          silhouet=255-invert
          s=s+1

          if not silhouet.size== 0:
            imgwrite(silhouet,dest_path)