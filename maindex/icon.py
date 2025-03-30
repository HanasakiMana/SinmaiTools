import os
from xml.dom.minidom import parse

titlePath = "D:/150/Package/Sinmai_Data/StreamingAssets/A000/icon"

verList = [
    'maimai でらっくす',
    'maimai でらっくす PLUS',
    'maimai でらっくす Splash',
    'maimai でらっくす Splash PLUS',
    'maimai でらっくす UNiVERSE',
    'maimai でらっくす UNiVERSE PLUS',
    'maimai でらっくす FESTiVAL',
    'maimai でらっくす FESTiVAL PLUS',
    'maimai でらっくす BUDDiES',
    'maimai でらっくす BUDDiES PLUS',
    'maimai でらっくす PRiSM',
    'maimai でらっくす PRiSM PLUS',
]

fileList = []
for folder in os.listdir(titlePath):
    if not os.path.isfile(titlePath + '/' + folder):
        fileList.append(titlePath + '/' + folder + '/Icon.xml')

genreList = []

genreAddVerList = [] # 由genreList的下标（genreId）确定

iconList = []

for file in fileList:
    dom = parse(file)
    data = dom.documentElement

    name = data.getElementsByTagName('name')[0].getElementsByTagName('str')[0].childNodes[0].nodeValue
    iconId = data.getElementsByTagName('name')[0].getElementsByTagName('id')[0].childNodes[0].nodeValue.zfill(6)
    genre = data.getElementsByTagName('genre')[0].getElementsByTagName('str')[0].childNodes[0].nodeValue
    obtainCondition = data.getElementsByTagName('normText')[0].childNodes[0].nodeValue

    addVersion = int(int(iconId[0:2]) / 5)

    if genre not in genreList:
        genreList.append(genre)
        genreAddVerList.append(addVersion)
    
    for genreId in range(len(genreList)):
        if genreList[genreId] == genre:
            iconList.append([genreId, iconId, name, obtainCondition, addVersion])

print(genreList)

iconList.sort(key=lambda x: x[1])

if os.path.exists(os.getcwd() + '/icon.md'):
    os.remove(os.getcwd() + '/icon.md')

with open('icon.md', 'wb') as f:

    # 按区域划分的目录
    f.write(f"## 区域目录\n\n".encode('utf-8'))
    currentVersion = -1
    for genreId in range(len(genreList)):
        if genreId != 1: # 排除RANDOM
            # print(currentVersion, genreAddVerList[genreId])
            if currentVersion != genreAddVerList[genreId]:
                currentVersion = genreAddVerList[genreId]
                f.write(f'\n### {verList[currentVersion]}\n\n'.encode('utf-8'))
            f.write(f'''- [{genreList[genreId]}](#{genreId})\n'''.encode('utf-8'))

    f.write(f"\n".encode('utf-8'))

    for genreId in range(len(genreList)):
        if genreId != 1: # 排除RANDOM
            f.write(f'## <span id="{genreId}">**{genreList[genreId]}**</span>\n\n'.encode('utf-8'))
            
            # 不同版本
            for verId in range(len(verList)): # 统计一下哪些版本没有称号
                iconListTemp = []
                for title in iconList:
                    if title[4] == verId and title[0] == genreId:
                        iconListTemp.append(title)

                # 跳过没有称号的版本
                if iconListTemp != []:
                    if genreId == 2: # 仅在实绩类型中显示版本
                        f.write(f'### <span id="ver_{verId}">**{verList[verId]}**</span>\n\n'.encode('utf-8'))

                    for title in iconListTemp:
                        iconId = title[1]
                        name = title[2]
                        obtainCondition = title[3]

                        f.write(
                            f'''<span id="titleId">**![{iconId}](https://r2.manalogues.com/icon/UI_Icon_{iconId}.png)**</span>

- **名称：**{name}
- **获取方式: **{obtainCondition}

'''.encode('utf-8')
                        )

