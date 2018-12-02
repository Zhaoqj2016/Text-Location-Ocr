# -*- coding: utf-8 -*-
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import shutil

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

img_dir = "mtwi_2018_task3_test/icpr_mtwi_task3/image_test"
txt_dir = "mtwi_2018_task3_test/results"
res_dir = "mtwi_2018_task3_test/AIE1003"
if os.path.exists(res_dir):
    shutil.rmtree(res_dir)
os.makedirs(res_dir)
txt_name = os.listdir(txt_dir)  # 列出文件夹下所有的目录与文件
for file in txt_name:
    file_path = os.path.join(txt_dir, file)
    with open(file_path, "r", encoding="utf-8") as txt_file:
        txt_list = txt_file.readlines()

        img_file = file[4:-4]
        img_file_path = os.path.join(img_dir, img_file)
        print(img_file)
        img = Image.open(img_file_path).convert('L') 
        results=[]
        res_path = os.path.join(res_dir, img_file[:-4]+'.txt')
        with open(res_path, "w",encoding="utf-8" ) as res_file:
            for txt in txt_list:
                box = txt.strip('\n').split(',')
                if len(box) < 4:
                    continue
                bbox = (int(box[0]),int(box[1]),int(box[2]),int(box[3]))
                cut_img = img.crop(bbox)
                #cut_img.save("Text-Location-Ocr/data/tmp/cut_img.jpg")
                # Simple image to string
                text = pytesseract.image_to_string(cut_img,lang='chi_sim')
                if text == '':
                    continue
                text=text.replace('\n','').replace('\r','')
                print(text)
                result=str(bbox[0])+','+str(bbox[1])+','+str(bbox[0])+','+str(bbox[3])+','\
                        +str(bbox[2])+','+str(bbox[1])+','+str(bbox[2])+','+str(bbox[3]) +',' + text+'\n'
                #results.append(result)
                res_file.write(result)
                #break
    #break



