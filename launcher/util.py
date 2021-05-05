import os
import hashlib
# 递归获取路径目录下的所有文件,默认情况下忽略以.开头的隐藏目录
# path 必须是路径
# ignore_path_prefix 是个数组,只需指定目录名的前缀


def list_all_files(path: str, ignore_path_prefix=["."]):
    p, n = os.path.split(path)
    if(n != "." and n != ".."):
        for ignore in ignore_path_prefix:
            if(n.startswith(ignore)):
                return []
    files = []
    for name in os.listdir(path):
        name = os.path.join(path, name)
        if os.path.isfile(name):
            files.append(name)
        elif os.path.isdir(name):
            files.extend(list_all_files(name))
    return files


# 计算文件的md5值
# filename 必须指定存在的文件


def get_md5(filename: str):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# 如果目录或文件所在的目录不存在,则递归创建
# pathname 路径或文件
def ensure_dir(pathname: str):
    directory = os.path.dirname(pathname)
    if not os.path.exists(directory):
        os.makedirs(directory)

# 使窗口在屏幕居中显示


def center_window(win, width, height):
    sw = win.winfo_screenwidth()
    # 得到屏幕宽度
    sh = win.winfo_screenheight()
    # 得到屏幕高度
    w = width
    h = height
    # 窗口宽高为100
    x = (sw-w) / 2
    y = (sh-h) / 2
    win.geometry("%dx%d+%d+%d" % (w, h, x, y))
