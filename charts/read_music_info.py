from ensurepip import version
import os
from xml.dom.minidom import parse

# 读取包含歌曲信息的xml文件
def read_xml(filePath):
    file = open(filePath)
    # 使用xml.dom.minidom生成DOM树
    DOMTree = parse(file)
    # 获取xml文件中的父级元素
    elements = DOMTree.documentElement

    # 通过读取子元素获取歌曲信息
    chartID = elements.getElementsByTagName('name')[0].getElementsByTagName('id')[0].childNodes[0].data
    musicName = elements.getElementsByTagName('name')[0].getElementsByTagName('str')[0].childNodes[0].data
    artist = elements.getElementsByTagName('artistName')[0].getElementsByTagName('str')[0].childNodes[0].data
    genre = elements.getElementsByTagName('genreName')[0].getElementsByTagName('str')[0].childNodes[0].data
    bpm = elements.getElementsByTagName('bpm')[0].childNodes[0].data
    bpm = int(bpm)
    addVersion = elements.getElementsByTagName('AddVersion')[0].getElementsByTagName('str')[0].childNodes[0].data
    
    # 定义变量用于获取谱面统计信息
    chartsDesigners = [] # 谱师
    levels = [] # 谱面等级 Basic/Advanced/Expert/Master(/Re:Master)
    ds = [] # 谱面定数
    maxNotes = [] # 谱面拥有的notes数

    # 读取子元素notesData
    notesData = elements.getElementsByTagName('notesData')[0].getElementsByTagName('Notes')

    # 读取各个谱面的相关信息
    for i in range(0, 5):
        # 切换到对应的note标签
        noteData = notesData[i]

        # 获得谱面等级
        level = noteData.getElementsByTagName('level')[0].childNodes[0].data
        # 在xml中曲目的定数以小数点后的数字保存
        levelDecimal = int(noteData.getElementsByTagName('levelDecimal')[0].childNodes[0].data)

        # 将各个谱面的数据append进刚才声明的变量
        if level != '0': # 校验白谱是否存在，白谱不存在的话level==0
            if levelDecimal >= 7: # 确定是否为带+的等级
                levels.append(level + '+')
            else:
                levels.append(level)
            # 定数
            ds.append(int(level) + levelDecimal/10)
        try:    
            chartsDesigners.append(noteData.getElementsByTagName('notesDesigner')[0].getElementsByTagName('str')[0].childNodes[0].data)
        except:
            chartsDesigners.append('-')

    # 由于水鱼和HDD内保存的版本分类信息不同，需要做替换
    genre_dict = {
        'maimai': 'maimai',
        'maimaiPLUS': 'maimai PLUS',
        'ORANGE': 'maimai ORANGE',
        'ORANGEPLUS': 'maimai ORANGE PLUS',
        'GreeN': 'maimai GreeN',
        'GreeNPLUS': 'maimai GreeN PLUS',
        'MURASAKi': 'maimai MURASAKi',
        'MURASAKiPLUS': 'maimai MURASAKi PLUS',
        'PiNK': 'maimai PiNK',
        'PiNKPLUS': 'maimai PiNK PLUS',
        'MiLK': 'maimai MiLK',
        'MiLKPLUS': 'MiLK PLUS',
        'FiNALE': 'maimai FiNALE',
        'maimaDX': 'maimai でらっくす',
        'maimaDXPLUS': 'maimai でらっくす PLUS',
        'Splash': 'maimai でらっくす Splash',
        'SplashPLUS': 'maimai でらっくす Splash Plus'
    }
    version = genre_dict.get(addVersion)
    if version == None:
        print(addVersion)

    # 保存到字典
    return {
        'title': musicName,
        'chartid': chartID,
        'artist': artist,
        'bpm': bpm,
        'genre': genre,
        'add_version': version,
        'level': levels,
        'ds': ds
    }

   
# 读取谱面信息的ma2文件
def read_ma2(filePath):
    tap, bReak, hold, slide, touch = 0, 0, 0, 0, 0
    notes = open(filePath).readlines()
    notes = [x[:-1] for x in notes] # 去除结尾的换行符\n
    notes.remove('')
    for line in notes:
        line = line.split('\t') # 利用空格符进行分割
        item = line[0]
        if item == 'T_NUM_TAP':
            tap = int(line[1])
        elif item == 'T_NUM_BRK':
            bReak = int(line[1]) # 大写第二个字母用于规避关键字
        elif item == 'T_NUM_HLD':
            hold = int(line[1])
        elif item == 'T_NUM_SLD':
            slide = int(line[1])
        elif item =='T_REC_TTP':
            touch = int(line[1])
    if touch == 0:
        output = [tap, hold, slide, bReak]
    else:
        output = [tap - touch, hold, slide, touch, bReak]
    return output


def read_info(directoryPath):
    file_list = os.listdir(directoryPath)
    notes = {}
    charts = []
    chartInfo = {}
    chartID = ''
    for file in file_list:
        file_suffix = file.split('.')[-1]
        if file == 'Music.xml':
            chartInfo = read_xml(directoryPath + '/' + file)
            chartID = chartInfo.get('chartid')
        elif file_suffix == 'ma2':
            difficulty_dict = {
                '00': 'Basic',
                '01': 'Advanced',
                '02': 'Expert',
                '03': 'Master',
                '04': 'Re:Master'
            }
            # 利用文件名后缀确定难度信息
            difficulty = difficulty_dict.get(file.split('.')[0].split('_')[-1])
            notes.update({difficulty: read_ma2(directoryPath + '/' + file)})
    # 依照难度信息对谱面信息排序
    for i in ['Basic', 'Advanced', 'Expert', 'Master', 'Re:Master']:
        charts.append(notes.get(i))
    # 如果白谱不存在，就把结尾的None删掉
    if charts[-1] == None:
        del charts[-1]
    chartInfo.update({'charts': charts})
    return {chartID: chartInfo}


if __name__ == '__main__':
    print(read_info('music011173'))
    print(read_info('SDEZ/music/music011143'))