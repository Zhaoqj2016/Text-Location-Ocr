"# Text-Location-Ocr" 

# 整体处理流程
## 1.执行textlocation.bat，将mtwi_2018_task3_test/icpr_mtwi_task3/image_test的图片使用cptn进行文本区域定位，保存文本的坐标位置到mtwi_2018_task3_test/results
## 2.执行python ocr.py, 从mtwi_2018_task3_test/results读取坐标位置信息，在mtwi_2018_task3_test/icpr_mtwi_task3/image_test读取图片文件，截取文本位置区域的图片，调用tesseract进行文本识别，识别结果保存到mtwi_2018_task3_test/AIE1003
