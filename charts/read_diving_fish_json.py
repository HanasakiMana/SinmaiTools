# 导入水鱼网站获取的json
import json


'''
    dict格式：
    title: 曲名
    type: 歌曲种类SD/DX
    ds: 定数[Basic, Advanced, Expert, Master(, Re:Master)]，数值类型是float
    level: 等级[Basic, Advanced, Expert, Master(, Re:Master)]，数值类型是str
    cids: 谱面id[1, 2, 3, 4(, 5)]
    charts: [
        {'notes': [TAP, HOLD, SLIDE, BREAK],
        'charter': '谱师'（没有就是'-'）
            } Basic
        {'notes': [TAP, HOLD, SLIDE, BREAK],
        'charter': '谱师'（没有就是'-'）
            } Advanced
        ……
        ]
    basic_info: {
        'title': '歌名',
        'artist': '曲师',
        'genre': '歌曲分类',
        'bpm': bpm,
        'release_date': '发布日期',
        'from': '版本',
        'is_new': Bool DX更新曲目
    }
    '''


def read_json(filePath):
    divingFish_musicData = json.loads(open(filePath).read())
    json_data = {}
    for i in divingFish_musicData: # 列表里的每一项都是一个字典
        dictData = read_dict(i) # 调用下面写的读取函数
        chartID = dictData.get('chartid')
        json_data.update({chartID: dictData}) # 以谱面id为key生成字典
    return json_data

   
def read_dict(dictionary):
    chartID = dictionary.get('id') # 谱面id
    chartType = dictionary.get('type') # 谱面类型
    ds = dictionary.get('ds') # 谱面定数
    level = dictionary.get('level') # 谱面等级
    charts = dictionary.get('charts')  # 谱面信息
    basicInfo = dictionary.get('basic_info') # 乐曲基本信息
    title = basicInfo.get('title') # 乐曲标题
    artist = basicInfo.get('artist') # 乐曲和BGM作者信息
    genre = basicInfo.get('genre') # 乐曲流派分类
    bpm = basicInfo.get('bpm')
    version = basicInfo.get('from') # 乐曲版本分类

    notes = []
    for dict in charts:
        notes.append(dict.get('notes'))

    return {
        'title': title,
        'chartid': chartID,
        'artist': artist,
        'bpm': bpm,
        'genre': genre,
        'add_version': version,
        'level': level,
        'ds': ds,
        'charts': notes
    }


if __name__ == '__main__':
    jsonData = read_json('diving-fish_musicData.json')
    print(jsonData.get('11143'))