#!/usr/bin/python
# coding:utf8

import os
import shutil
import uuid
def dirlist(path, allfile):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            print (filepath)
            if filepath.endswith('JPG'):
                move_File(filepath)
        # allfile.append(filepath)
    return allfile
# 移动文件


def move_File(FilePath):
    basePath = "C:\\Users\\localhost\\Desktop\\新建文件夹\\新建文件夹\\"
    oldFilePath = FilePath  # 原文件位置
    newFilePath = basePath+str(uuid.uuid1()).replace("-", "").upper()+'.JPG'    # 移动到
    print(oldFilePath)
    print(newFilePath)
    print("*"*100)
    shutil.copyfile(oldFilePath, newFilePath)


print(dirlist('C:\\Users\\localhost\\Desktop\\新建文件夹\\CPLAssets', []))
