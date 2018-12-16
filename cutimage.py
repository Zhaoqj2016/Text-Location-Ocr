# -*- coding: UTF-8 -*-
 
import numpy as np
import cv2
import math
import os
import shutil

 
## 图片旋转
def rotate_bound(image, x1,y1,x2,y2,x3,y3,x4,y4):
    (h, w) = image.shape[:2]
    (cX, cY) = ((y4-x2)/2+x2, (y1-y3)/2+y3)
    cX = x1
    cY = y1
    #print("cX=",cX," cY=",cY)
    angle=math.degrees(math.asin((y1-y4)/math.sqrt((y1-y4)**2 + (x4-x1)**2)))
    #print(angle)
    # 提取旋转矩阵 sin cos 
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    #第三个参数：变换后的图像大小
    return cv2.warpAffine(image,M,(w*2,h))
 
 #调整坐标顺序为：
 #  x2,y2    x3,y3
 #  x1,y1    x4,y4
def original_coordinate_transformation(x1,y1,x2,y2,x3,y3,x4,y4):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    x3 = float(x3)
    y3 = float(y3)
    x4 = float(x4)
    y4 = float(y4)
    #判断x1和x3大小，x3调整为大的数
    if x1 > x3:
        y = y1
        x = x1
        y1 = y3
        x1 = x3
        y3 = y
        x3 = x
    #判断x2和x4大小，x4调整为大的数
    if x2 > x4:
        y = y4
        x = x4
        y4 = y2
        x4 = x2
        y2 = y
        x2 = x
    #判断y1和y2大小，y1调整为大的数
    if y2 > y1:
        y = y1
        x = x1
        y1 = y2
        x1 = x2
        y2 = y
        x2 = x
    #判断y3和y4大小，y4调整为大的数
    if y3 > y4:
        y = y3
        x = x3
        y3 = y4
        x3 = x4
        y4 = y
        x4 = x
    return x1,y1,x2,y2,x3,y3,x4,y4

#返回翻转图片 后 裁剪的坐标
# newx1,newy1     -
# -               newx2,newy2
def clip_coordinates(x1,y1,x2,y2,x3,y3,x4,y4):
    newx1 = x1
    newx2 = x1+math.sqrt((x4-x1)**2+(y1-y4)**2)
    newy1 = y1-math.sqrt((x1-x2)**2+(y1-y2)**2)
    newy2 = y1
    return newx1,newy1,newx2,newy2

img_dir = "mtwi_2018_train/error_image"
txt_dir = "mtwi_2018_train/txt_train"
res_dir = "mtwi_2018_train/train_image"
if os.path.exists(res_dir):
   shutil.rmtree(res_dir)
os.makedirs(res_dir)
img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
for file in img_name:
    image_path = os.path.join(img_dir, file)#"./mtwi_2018_train/image_train/T1._WBXtXdXXXXXXXX_!!0-item_pic.jpg.jpg"
    try:
        image = cv2.imread(image_path)
        text_path = os.path.join(txt_dir, file[:-4]+".txt")#./mtwi_2018_train/txt_train/T1._WBXtXdXXXXXXXX_!!0-item_pic.jpg.txt"
        with open(text_path,"r", encoding="utf-8") as f:
            lines = f.readlines()
            count = -1
            for line in lines:
                count = count + 1
                print("count=",count)
           
                (x1,y1,x2,y2,x3,y3,x4,y4,text)=line.split(",")
                x1,y1,x2,y2,x3,y3,x4,y4 = original_coordinate_transformation(x1,y1,x2,y2,x3,y3,x4,y4)
                newx1,newy1,newx2,newy2 = clip_coordinates(x1,y1,x2,y2,x3,y3,x4,y4)
                rotated = rotate_bound(image,x1,y1,x2,y2,x3,y3,x4,y4) #将图片翻转
                cropImg = rotated[int(newy1):int(newy2),int(newx1):int(newx2)]#裁剪
                cv2.imwrite("mtwi_2018_train/test/cropImg.jpg", cropImg)
        
                save_file = os.path.join(res_dir,file[:-4]+"__"+("%03d"%count)+".jpg")
                
                cv2.imwrite(save_file, cropImg)
          
    except Exception as e:
        print("error file=",file,"e=",e)
        with open("errlog2.txt","a", encoding="utf-8") as f:
            f.write(file+"\n")
        

