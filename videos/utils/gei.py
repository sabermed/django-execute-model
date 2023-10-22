import os
import cv2
import numpy as np
import PIL # import Image
import math

def imgwrite(img,dest_path0):
  filename = dest_path0+'.jpg'
  cv2.imwrite(os.path.join(dest_path,filename), img) # add the destination folder path


def calculate_centroids(binary_image):
  binary_image= binary_image/255
  sum_x = 0
  sum_y = 0
  count = 0

  for y in range(binary_image.shape[0]):
      for x in range(binary_image.shape[1]):
          if binary_image[y, x] == 1:
              sum_x += x
              sum_y += y
              count += 1

  centroid_x = sum_x / count
  centroid_y = sum_y / count

  return centroid_x, centroid_y


######### loop over all png images of 180 degrée files########
folder_path = '/content/drive/MyDrive/PD-90-Silhouet'
for file_name in os.listdir(folder_path):
  file_path = os.path.join(folder_path, file_name)
  dest_path0=(file_name.split('-')[0]+'-'+file_name.split('-')[1]+'-'+file_name.split('-')[2]+'-'+file_name.split('-')[3])
  dest_path=('/content/drive/MyDrive/PD-90-GEI')
  if not os.path.exists(os.path.join(dest_path,dest_path0+'.jpg')):
    sum_silh=0
    for s in range(15,46):
      file_path1 = os.path.join(file_path,str(s)+'.jpg')
      ##################RESIZING WITH  WIDTH-HEIGTH RATIO KEEPING######################
      fixed_height = 600
      image = PIL.Image.open(file_path1)
      height_percent = (fixed_height / float(image.size[1]))
      width_size = int((float(image.size[0]) * float(height_percent)))
      image = image.resize((width_size, fixed_height))
      img_array = np.array(image)
      ################## END END RESIZING WITH  WIDTH-HEIGTH RATIO KEEPING#####################
      c1,c2=calculate_centroids(img_array)
      y,x=img_array.shape
      x1=250-math.ceil(c1)
      a=np.zeros((600,x1),'int')
      lawla=np.hstack((a,img_array))
      x2=250+math.ceil(c1)-x
      b=np.zeros((600,x2),'int')
      thania=np.hstack((lawla,b))
      t=400-math.ceil(c2)
      l=np.zeros((t,500),'int')
      ltaht=np.vstack((thania,l))
      f=400+math.ceil(c2)-y
      lf=np.zeros((f,500),'int')
      silhouet=np.vstack((lf,ltaht))
      sum_silh=sum_silh+silhouet
    GEI=sum_silh/40
    if not GEI.size== 0:
      imgwrite(GEI,dest_path0)