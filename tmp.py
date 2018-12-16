# -*- coding: UTF-8 -*-
 
import numpy as np
import cv2
import math
import os
import shutil
import util as util
import GlobParameter as GbPara
img_dir = GbPara.img_dir
txt_dir = GbPara.txt_dir
res_dir = GbPara.res_dir

if os.path.exists(res_dir):
   shutil.rmtree(res_dir)
os.makedirs(res_dir)
img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
for file in img_name:
    image_path = os.path.join(img_dir, file) #tmp/row_image/T1.3BPFFJdXXXXXXXX_!!0-item_pic.jpg.jpg

    try:
        image = cv2.imread(image_path)
        text_path = os.path.join(txt_dir, file[:-4]+".txt")
        with open(text_path,"r", encoding="utf-8") as f:
            lines = f.readlines()
            count = -1
            for line in lines: #41.67,506.73,41.67,564.51,715.61,564.51,715.61,506.73,上海道冠五金有限公司
                (x1,y1,x2,y2,x3,y3,x4,y4,text)=line.split(",")
                x1,y1,x2,y2,x3,y3,x4,y4 = util.original_coordinate_transformation(x1,y1,x2,y2,x3,y3,x4,y4)
                newx1,newy1,newx2,newy2 = util.clip_coordinates(x1,y1,x2,y2,x3,y3,x4,y4)
                rotated = util.rotate_bound(image,x1,y1,x2,y2,x3,y3,x4,y4) #将图片翻转
                cropImg = rotated[int(newy1):int(newy2),int(newx1):int(newx2)]#裁剪
                util.create_lable_img_dir(text, res_dir, cropImg)
                count = count + 1
    except Exception as e:
        print("error file=",file,"e=",e)
        with open("errlog2.txt","a", encoding="utf-8") as f:
            f.write(file+"\n")
        

