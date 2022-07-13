import UnityPy
from PIL import Image
import os


# 解.assets包
def unpackAssets(filePath: str, assetType: str, savePath: str):
    print(f'Unpacking {assetType} files in {filePath}...')
    env = UnityPy.load(filePath)
    try:
        os.mkdir(savePath + f'/{assetType}')
    except:
        pass
    for obj in env.objects:
        if obj.type.name == assetType:
            data = obj.read()
            fileName = data.name
            data.image.save(savePath + f'/{assetType}/{fileName}.png')
    print('Complete!')


# 解AssetBundleImages
def unpackAssetBundleImages(dirPath: str, savePath: str):
    try:
        os.mkdir(savePath + '/AssetBundleImages')
    except:
        pass
    os.chdir(dirPath)
    dirs = os.listdir()
    for dir in dirs:
        if os.path.isdir(dirPath + f'/{dir}'):
            try:
                os.mkdir(savePath + f'/AssetBundleImages/{dir}')
            except:
                pass
            os.chdir(dirPath + f'/{dir}')
            files = os.listdir()
            currentDir = os.getcwd()
            print(f'Unpacking Texture2D files in {currentDir}...')
            for file in files:
                # 查找ab文件
                if file.split('.')[-1] == 'ab':
                    print(f'Unpacking {file}')
                    env = UnityPy.load(currentDir + f'/{file}')
                    for obj in env.objects:
                        if obj.type.name == 'Texture2D':
                            data = obj.read()
                            fileName = data.name
                            data.image.save(savePath + f'/AssetBundleImages/{dir}/{fileName}.png')
            print('Complete!')
                    


# 解包
def unpack(hddPath: str, savePath: str):
    resources_path = '/Package/Sinmai_Data/resources.assets'
    sharedAssets0_path = '/Package/Sinmai_Data/sharedassets0.assets'
    
    # 读取 resources.assets
    try:
        os.mkdir(savePath + '/resources')
    except:
        pass
    unpackAssets(hddPath + resources_path, 'Texture2D', savePath + '/resources')
    unpackAssets(hddPath + resources_path, 'Sprite', savePath + '/resources')
    

    # 读取 sharedassets0.assets
    try:
        os.mkdir(savePath + '/sharedassets0')
    except:
        pass
    unpackAssets(hddPath + sharedAssets0_path, 'Texture2D', savePath + '/sharedassets0')
    unpackAssets(hddPath + sharedAssets0_path, 'Sprite', savePath + '/sharedassets0')


    # 解整个AssetBundle（AB包）
    abPath = '/Package/Sinmai_Data/StreamingAssets/A000/AssetBundleImages'
    unpackAssetBundleImages(hddPath + abPath, savePath)



if __name__ == '__main__':
    hddPath = '/Volumes/SC001/SDEZ/125'
    savePath = '/Users/mallow/Documents/125assets'
    unpack(hddPath, savePath)

    