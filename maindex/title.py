import os
from xml.dom.minidom import parse

titlePath = "D:/150/Package/Sinmai_Data/StreamingAssets/A000/title"

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
        fileList.append(titlePath + '/' + folder + '/title.xml')

genreList = []

rareTypeList = []

titleList = []

for file in fileList:
    dom = parse(file)
    data = dom.documentElement

    name = data.getElementsByTagName('name')[0].getElementsByTagName('str')[0].childNodes[0].nodeValue
    titleId = data.getElementsByTagName('name')[0].getElementsByTagName('id')[0].childNodes[0].nodeValue.zfill(6)
    genre = data.getElementsByTagName('genre')[0].getElementsByTagName('str')[0].childNodes[0].nodeValue
    obtainCondition = data.getElementsByTagName('normText')[0].childNodes[0].nodeValue
    rareType = data.getElementsByTagName('rareType')[0].childNodes[0].nodeValue

    addVersion = int(int(titleId[0:2]) / 5)

    if genre not in genreList:
        genreList.append(genre)
    if rareType not in rareTypeList:
        rareTypeList.append(rareType)
    
    for i in range(len(genreList)):
        if genreList[i] == genre:
            for j in range(len(rareTypeList)):
                if rareTypeList[j] == rareType:
                    titleList.append([i, titleId, name, obtainCondition, addVersion, j])

print(genreList)
print(rareTypeList)

titleList.sort(key=lambda x: x[0])


if os.path.exists(os.getcwd() + '/title.md'):
    os.remove(os.getcwd() + '/title.md')

def changeTitleColor(name: str, rareType):

    if rareType == 0: # normal
        colorHex = '#CECECE'
    elif rareType == 1: # bronze
        colorHex = '#CD950C'
    elif rareType == 2: # Silver
        colorHex = '#F0F8FF'
    elif rareType == 3: # gold   
        colorHex = '#FFD700'
    else: # rainbow
        return f'''<font style="background-image: linear-gradient(to right, #E4080A, #FE9900, #FFDE59, #7DDA58, #98F5F9, #5DBFE9, #CC6CE7)">{name}</font>'''
    
    return f'''<font style="background-color: {colorHex}"> {name} </font>'''

with open('title.md', 'wb') as f:

    for genreId in range(len(genreList)):
        if genreId != 1:
            f.write(f'''- [{genreList[genreId]}](#{genreId})\n'''.encode('utf-8'))

    f.write(f"\n".encode('utf-8'))

    for genreId in range(len(genreList)):
        if genreId != 1: # 不同种类

            f.write(f'## <span id="{genreId}">**{genreList[genreId]}**</span>\n\n'.encode('utf-8'))
            
            # 不同版本
            for verId in range(len(verList)):
                titleListTemp = []
                for title in titleList:
                    if title[4] == verId and title[0] == genreId:
                        titleListTemp.append(title)

                # 跳过没有称号的版本
                if titleListTemp != []:
                    f.write(f'### <span id="ver_{verId}">**{verList[verId]}**</span>\n\n'.encode('utf-8'))

                    for title in titleListTemp:
                        titleId = title[1]
                        name = title[2]
                        obtainCondition = title[3]
                        addVersion = title[4]
                        rareType = title[5]

                        f.write(
                            f'''<span id="titleId">**{changeTitleColor(name, rareType)}**</span>

- **获取方式:** {obtainCondition}

'''.encode('utf-8')
                        )

