# 生成用于MiaBot的sqlite配置文件
import os
import datetime, pytz
import sqlite3
from read_music_info import readChart

# 获取指定文件夹目录的文件列表，并且避免相对路径引发的问题
def getFileList(dirPath):
    currentPath = os.getcwd()
    os.chdir(dirPath)
    fileList = os.listdir()
    os.chdir(currentPath)
    return fileList

# 读取hdd中的谱面文件
def readHDD(filePath: str):
    filesList = os.listdir(filePath)
    hddData = {}
    for files in filesList:
        if len(files.split('.')) == 1: # 排除文件留下文件夹
            if files not in ['music000000', 'music000001']: # 排除两个教程谱面
                hddData.update(readChart(filePath + '/' + files))
    return hddData

# 合并出来歌曲信息
def geneMusicInfo(hddData: dict):
    musicInfo = {}
    chartTypeData = {} # 独立记录dx和std的谱面id
    musicInfoList = []

    for chartId, data in hddData.items():
        isDX = False # 是否是DX谱面的flag
        if len(chartId) == 5: # DX谱面
            isDX = True
            musicId = str(int(chartId[1:])) # 去除字符串开头多余的0
        else:
            musicId = chartId

        title = data.get('title')
        artist = data.get('artist')
        genre = data.get('genre')
        bpm = data.get('bpm')
        addVersion = data.get('add_version')

        musicInfo.update({musicId: [title, artist, genre, bpm, addVersion, 0]})

        if chartTypeData.get(musicId) == None:
                if not isDX:
                    chartTypeData.update({musicId: [chartId, 'NULL']})
                if isDX:
                    chartTypeData.update({musicId: ['NULL', chartId]})
        else:
            original = chartTypeData.get(musicId)
            if not isDX:
                chartTypeData.update({musicId: [chartId, original[1]]})
            if isDX:
                chartTypeData.update({musicId: [original[0], chartId]})

    # 合并信息
    for musicId, chartType in chartTypeData.items():
        musicData = musicInfo.get(musicId)
        musicInfoList.append([musicId] + musicData + chartType)
    
    musicInfoList.sort(key=lambda x: int(x[0]))

    return(musicInfoList)


# 生成谱面信息
def geneChartInfo(hddData: dict):
    chartInfo = []
    diffList = ['basic', 'advanced', 'expert', 'master', 'reMaster']
    for chartId, data in hddData.items():

        isDX = False # 是否是DX谱面的flag
        if len(chartId) == 5: # DX谱面
            isDX = True
            musicId = chartId[1:]
            while musicId[0] == 0:
                musicId = musicId[1:]
                assert len(musicId) >= 1
        else:
            musicId = chartId
        
        level = data.get('level')
        ds = data.get('ds')
        charters = data.get('charter')
        charts = data.get('charts')

        assert len(level) == len(ds) == len(charters) == len(charts)

        for i in range(len(level)):
            if isDX:
                chartType = 'DX'
            else:
                chartType = 'SD'
            
            chart = charts[i]
            tapCount = chart[0]
            holdCount = chart[1]
            slideCount = chart[2]
            touchCount = chart[3]
            breakCount = chart[4]
            
            if touchCount == 0:
                touchCount = 'NULL'
            diff = diffList[i]
            chartLevel = level[i]
            chartDs = ds[i]
            charter = charters[i]

            chartInfo.append([chartId, chartType, musicId, diff, chartLevel, chartDs, charter, tapCount, holdCount, slideCount, touchCount, breakCount])
    chartInfo.sort(key=lambda x: int(x[0]))
    return chartInfo
        
        
            
# 创建sqlite
def createSqlite(sqlPath: str, dbPath: str):
    with open(sqlPath, 'r') as sqlFile:
        sqlCmd = sqlFile.readlines()
        sqlCmd = "".join(sqlCmd)
    if os.path.exists(dbPath):
        os.remove(dbPath)
    conn = sqlite3.connect(dbPath)
    cur = conn.cursor()
    cur.executescript(sqlCmd)
    conn.commit()
    conn.close()


# 向sqlite添加数据
def updateSqlite(dbPath: str, ver: str, musicData: list = None, chartData: list = None):
        
        cmdList = [] # 需要执行的命令列表
        
        # 一个用来拼接出sql命令的小函数
        def joinCmd(id, info, targetTable):
            if id != None:
                data = f"\'{id}\'"
            else:
                data = ''
            for i in info:
                # 给str套单引号，不然sql不认为是TEXT类型
                if isinstance(i, str):
                    # 如果曲名中出现了单引号，就需要把单引号打两遍，第一个相当于转义符
                    i = i.replace('\'', r"''")
                    # 套引号
                    if i != 'NULL':
                        i = f"\'{i}\'"
                data += f', {i}'
            return f'INSERT INTO {targetTable} VALUES({data})'

        # musicInfo
        for data in musicData:
            musicId = data[0]
            musicInfo = data[1:]
            cmdList.append(joinCmd(musicId, musicInfo, 'musicInfo'))

        # chartInfo
        for data in chartData:
            chartId = data[0]
            chartInfo = data[1:]
            cmdList.append(joinCmd(chartId, chartInfo, 'chartInfo'))
        # dbInfo
        updateTime = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        cmdList.append(f"INSERT INTO dbInfo VALUES('{updateTime}')")
        # dataVersion
        cmdList.append(f"INSERT INTO dataVersion VALUES(\'{ver}\')")
        # 执行命令
        conn = sqlite3.connect(dbPath)
        cur = conn.cursor()
        # 清空表
        cur.execute('DELETE FROM musicInfo')
        cur.execute('DELETE FROM chartInfo')
        cur.execute('DELETE FROM dbInfo')
        for cmd in cmdList:
            print(cmd)
            cur.execute(cmd)
            conn.commit()
        conn.close()




if __name__ == '__main__':
    chartPath = 'charts/SDEZ/music'
    sqlPath = 'SDEZ.sql'
    dbPath = 'SDEZ.sqlite'
    createSqlite(sqlPath, dbPath)
    
    data = readHDD(chartPath)
    
    musicData = geneMusicInfo(data)
    chartData = geneChartInfo(data)

    
    updateSqlite(dbPath, 'DX1.30', musicData, chartData)
