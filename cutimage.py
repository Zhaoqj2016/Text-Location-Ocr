# -*- coding: UTF-8 -*-
 
import numpy as np
import cv2
import math

 
## 图片旋转
def rotate_bound(image, x1,y1,x2,y2,x3,y3,x4,y4):
    (h, w) = image.shape[:2]
    (cX, cY) = ((y4-x2)/2+x2, (y1-y3)/2+y3)
    cX = x1
    cY = y1
    print("cX=",cX," cY=",cY)
    angle=math.degrees(math.asin((y1-y4)/math.sqrt((y1-y4)**2 + (x4-x1)**2)))
    print(angle)
    # 提取旋转矩阵 sin cos 
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    #第三个参数：变换后的图像大小
    return cv2.warpAffine(image,M,(w,h))
 
path = "data\mtwi_2018_train\image_train"

image_path = "./t2/T1._WBXtXdXXXXXXXX_!!0-item_pic.jpg.jpg"
image = cv2.imread(image_path)
text_path = "./t2/T1._WBXtXdXXXXXXXX_!!0-item_pic.jpg.jpg.txt"
with open(text_path,encoding="utf-8") as f:
    lines = f.readlines()
(x1,y1,x2,y2,x3,y3,x4,y4,text)=lines[0].split(",")
print(type(image),image.shape,image.size, image.dtype)
x1 = float(x1)
y1 = float(y1)
x2 = float(x2)
y2 = float(y2)
x3 = float(x3)
y3 = float(y3)
x4 = float(x4)
y4 = float(y4)
newx1 = x1
newx2 = x1+math.sqrt((x4-x1)**2+(y1-y4)**2)
newy1 = y1-math.sqrt((x1-x2)**2+(y1-y2)**2)
newy2 = y1
print("newx1",newx1,newx2,newy1,newy2)
rotated = rotate_bound(image,x1,y1,x2,y2,x3,y3,x4,y4)
cropImg = rotated[(newy1):(newy2),(newx1):(newx2)]
cv2.imshow("imput", image)
cv2.imshow("output", rotated)

cv2.imwrite("t2/rotated.jpg", rotated)
cv2.imshow("cropImg", cropImg)
cv2.imwrite("t2/cropImg.jpg", cropImg)
cv2.waitKey(0)

