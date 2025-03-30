import os
from shutil import copyfile
import tempfile
import time

filePath = r'C:\SDDT150\package\mu3_Data\StreamingAssets\GameData\A016\musicsource\musicsource7157'
hcaexePath = r'C:\Users\mana\Documents\GitHub\SinmaiTools\acb_decode'

os.chdir(filePath)
fileList = os.listdir()

# 统计属于音乐的acb文件
acbList = []
for fileName in fileList:
    if fileName[0:5] == 'music' and fileName[-3:] == 'acb' and fileName[5:11] != '000000' and fileName[5:11] != '000001':
        acbList.append(fileName)
print(acbList)

startTime = time.time()
count = 0
for fileName in acbList:
    count += 1
    # 获取歌曲id
    musicID = fileName.split('.')[0][-4:]
    while musicID[0] == '0':
        musicID = musicID[1:]
    # 生成一个存储hca文件的临时文件夹
    tmpPath = tempfile.mkdtemp()
    acbPath = filePath + rf'\{fileName}'
    # 这里执行的是pip安装的acb-py
    print(f'python -m acb {acbPath} {tmpPath}')
    os.system(f'python -m acb {acbPath} {tmpPath}')
    hcaPath = tmpPath +rf'\music.hca'
    # 切换到hca.exe的目录并执行hca2wav操作
    os.chdir(hcaexePath)
    os.system(rf'.\hca {hcaPath} -a E0748978 -b CF222F1F')
    # 保存导出的wav文件
    copyfile(tmpPath + rf'\music.wav', rf'{hcaexePath}\{musicID}.wav')
    # 统计信息
    print('\n')
    print(rf'music id: {musicID}')
    print(rf'{count}/{len(acbList)}')
    print('Aready took ' + str(int(time.time() - startTime)) + 's')
    print('\n')
    