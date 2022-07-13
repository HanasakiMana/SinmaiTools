import os
from shutil import copyfile
import tempfile
import time

filePath = r'E:\SDEZ\125\Package\Sinmai_Data\StreamingAssets\A000\SoundData'
hcaexePath = r'C:\Users\Mallow-GamingMachine\Desktop\acb_decode'

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
    os.system(f'python -m acb {acbPath} {tmpPath}')
    hcaPath = tmpPath +rf'\Play.hca'
    # 切换到hca.exe的目录并执行hca2wav操作
    os.chdir(hcaexePath)
    os.system(rf'.\hca {hcaPath} -a 9DF55E68 -b 7F455149')
    # 保存导出的wav文件
    copyfile(tmpPath + rf'\Play.wav', rf'E:\acb_decode\{musicID}.wav')
    # 统计信息
    print('\n')
    print(rf'music id: {musicID}')
    print(rf'{count}/{len(acbList)}')
    print('Aready took ' + str(int(time.time() - startTime)) + 's')
    print('\n')
    