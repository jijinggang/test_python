#!python
import zipfile
import os

# 把多个文件打包成zip


def zipfiles(zipname, files, is_add=False):
    mode = 'w'
    if is_add:
        mode = 'a'
    with zipfile.ZipFile(zipname, mode, zipfile.ZIP_DEFLATED) as zp:
        for file in files:
            zp.write(file)

# 把一个文件夹打包成zip


def zippath(zipname, path):
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zp:
        for root, dirs, files in os.walk("d:/_m"):
            for file in files:
                zp.write(root+"/"+file)

# 向现有zip中添加文件


def addtozip(zipname, files):
    zipfiles(zipname, files, True)


# add files here
if(__name__ == '__main__'):
    addtozip("1.zip", ["1.exe"])
