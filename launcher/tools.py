import os
import util
import shutil
# 根据路径一键生成发布包目录


def gen_release_package(dir):
    infos = get_file_infos(dir)
    new_dir = dir+"\\..\\"+os.path.basename(dir)+"_filelist\\"
    if(os.path.exists(new_dir)):
        shutil.rmtree(new_dir)
    util.ensure_dir(new_dir)
    gen_list_file(infos, new_dir)
    copy_all_files(dir, new_dir, infos)

# 遍历查找所有文件的相对路径/大小/md5


def get_file_infos(dir):
    files = util.list_all_files(dir)
    infos = []
    for file in files:
        relfile = os.path.relpath(file, dir)
        md5 = util.get_md5(file)
        size = os.path.getsize(file)
        infos.append((relfile, size, md5))
    return infos


# 生成filelist.txt


def gen_list_file(infos, new_dir):
    lines = []
    for relfile, size, md5 in infos:
        s = relfile+":" + str(size)+":" + md5
        lines.append(s)
    txt = "\n".join(lines)
    print(txt)

    with open(new_dir+"\\filelist.txt", 'w+', encoding='utf-8') as f:
        f.write(txt)

# 复制并命名所有文件,放到新目录


def copy_all_files(dir, new_dir, infos):
    for relfile, size, md5 in infos:
        shutil.copy(os.path.join(dir, relfile),
                    os.path.join(new_dir, md5+".bin"))
    pass


gen_release_package("D:\\github.com\\test_python\\dist")
