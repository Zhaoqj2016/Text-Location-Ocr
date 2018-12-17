import math
import os
import random
import cv2
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

# path 全路径
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

#创建指定目录
def create_dir_lable(father_dir_path, dir_name):
    path = father_dir_path + "/" + dir_name
    mkdir(path)
    return path

def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def create_lable_img_dir(string, father_dir_path, img):
    img_shape = img.shape
    img_l = img_shape[1]
    img_h = img_shape[0]
    size = len(string) - 1
    step = img_l / size
    start_l = 0
    end_l = int(step)

    print(img_l, img_h, string, size, step)
    # print([x for x in string], len(string))
    for c in string :
        is_chinese_flag = is_chinese(c)
        if is_chinese_flag:
            start_l = max(start_l - 1 , 0)
            end_l = min(end_l + 1, img_l)

        cropImg = img[:,int(start_l):int(end_l)]#裁剪

        if is_chinese_flag:
            cv2.imshow("cropImg", cropImg)
            cv2.waitKey(0)

        start_l += step
        end_l += step

        path = create_dir_lable(father_dir_path, str(c))
        save_img_file_name = path + "/" + str(random.randint(0,10000)) + ".jpg"
        print(save_img_file_name)
        cv2.imwrite(save_img_file_name, cropImg)



# 一个大的截图一个目录 并生成每个字的标签
def create_dir_save_four_word_img_file(string, father_dir_path, img):
    string = string.replace("\n", "")
    path = create_dir_lable(father_dir_path, string)
    save_img_file_name = path  +"/" + string + ".jpg"
    print(save_img_file_name)
    cv2.imwrite(save_img_file_name, img)
    return

if __name__ == "__main__":
    # tmp = is_chinese("h")
    # print(tmp)

    # print(min(12 - 1,15))
    # print(max(12,15))
    pass    