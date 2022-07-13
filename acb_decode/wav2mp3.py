import os

filePath = 'E:/acb_decode'
savePath = filePath + '/mp3'
os.chdir(filePath)
fileList = os.listdir()
for file in fileList:
    fileName = file.split('.')[0]
    os.system(f"ffmpeg -i {filePath + '/' + file} -ar 44.1k -b:a 192k {savePath + '/' + fileName + '.mp3'}")
