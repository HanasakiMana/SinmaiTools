from read_music_info import readChart
from read_diving_fish_json import read_json
import os


# CONST
SDGB = 'SDGB/music'
SDEZ = 'SDEZ/music'
jsonData = read_json('diving-fish_musicData.json')


# 读取hdd中的谱面文件
def read_hdd(filePath):
    filesList = os.listdir(filePath)
    hddData = {}
    for files in filesList:
        if len(files.split('.')) == 1:
            hddData.update(readChart(filePath + '/' + files))
    return hddData


def compare(hdd_dict, json_dict):
    # 最终的输出字典
    full_dict = {}
    
    # 创建谱面id的并集
    full_id_dict = {}
    for key in hdd_dict.keys():
        full_id_dict.setdefault(key)
    for key in json_dict.keys():
        full_id_dict.setdefault(key)

    # 利用谱面id对hdd和json的数据进行遍历，并加入相关比较项的参数
    for key in full_id_dict.keys():
        hddData = hdd_dict.get(key)
        jsonData = json_dict.get(key)
           
        
        if hddData == jsonData: # 二者完全相同，直接update进字典
            full_dict.update({key: hddData}) 

        elif hddData == None and jsonData != None: # json有而HDD没有，说明该曲目已经被删除
            jsonData.update({'isDeleted': True})
            full_dict.update({key: jsonData})

        elif jsonData == None and hddData != None: # HDD有而json没有，说明这是首国服没有上的歌
            hddData.update({'unReleased': True})
            full_dict.update({key: hddData})

        elif hddData != None and jsonData != None: # 二者均有值，则说明有不同的部分
            comparedData = {}
            for keys in hddData.keys(): # 遍历字典，将相同的值写入comparedData
                
                if hddData.get(keys) == jsonData.get(keys):
                    comparedData.update({keys: hddData.get(keys)})
            
            difference = {}
            for keys in hddData.keys(): # 再次遍历，找出不同的值（由于存在追加谱面，因此不能只比较谱面等级和定数）
                if hddData.get(keys) != jsonData.get(keys) and keys != 'add_version': # 后者用于判断不同是否来自于版本差异（SDGB和SDEZ的加入版本有差异）
                    difference.update({
                            keys: {
                                'hdd': hddData.get(keys),
                                'json': jsonData.get(keys)
                            }
                        }
                    )
            if len(difference): # 避免由于仅出现add_version的差异导致difference为空
                comparedData.update({'chart_change': difference})
                full_dict.update({key: comparedData})
    return full_dict



if __name__ == '__main__':
    full_dict = compare(read_hdd(SDEZ), jsonData)
    for value in full_dict.values():
        if value.get('add_version') == 'Universe':
            print(value)