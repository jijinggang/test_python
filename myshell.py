import json
import os
import sys
import subprocess
import hashlib


def pause():
    os.system('pause')


def pause_and_exit(status):
    pause()
    sys.exit(status)


# 模拟shell脚本的call
# cmd 命令行,各参数用空格隔开,例如"ls -a /"
# dir 设置执行命令的当前路径
# exit_on_error 如果为True,则执行脚本退出码不为0时,自动暂停,等用户按任意键后退出
def call(cmd: str, dir=None, exit_on_error=True):
    if dir == None:
        dir = os.getcwd()
    proc = subprocess.run(cmd, shell=True, cwd=dir)
    code = proc.returncode
    if exit_on_error and code != 0:
        print(f"CALL ERROR {code}:", cmd)
        pause_and_exit(code)
    return code


# 获取给定目录或文件的svn当前版本号
# pathfile 如果是目录,则返回该目录下所有文件的最新svn版本号,如果是文件,则返回该文件的最新版本号
# 返回的版本号是字符串
def svn_version(pathfile: str) -> str:
    proc = subprocess.run(
        f'svn info "{pathfile}"', shell=True, stdout=subprocess.PIPE)
    import re
    txt = proc.stdout.decode('gbk')
    versions = re.findall("^Revision: (\d+)", txt, re.M)
    try:
        version = versions[0]
    except IndexError:
        sys.exit(txt)
    return version


# 计算文件的md5值
# filename 必须指定存在的文件
def md5(filename: str):
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


# 根据文件或svn版本号检查源文件是否改变,为增量编译提供支持,只有输入和输出的所有文件都没有变化时,才判定为无变化
class CheckChange:

    # inputs 必须是列表,每一项可以是文件或目录,如果是目录则表示包含目录内的所有文件
    # outputs 必须是列表,每一项可以是文件或目录,如果是目录则表示包含目录内的所有文件
    # key 根据key来指定缓存信息的存放位置,一般应指定为__file__
    # check_file_not_svn 为True表示直接检查输入所有文件的md5,为false则表示用输入文件的svn版本号来判断是否修改; 无论如何设置,对输出文件都会直接用文件的md5来判定
    def __init__(self, inputs: list, outputs: list, key: str, check_file_not_svn=True):

        self.file = os.path.join(os.getcwd(), ".checkdb", key+".db")
        ensure_dir(self.file)
        self.inputs = inputs
        self.outputs = self._compute_files(outputs)
        self.md5 = md5
        self.getsize = os.path.getsize
        if check_file_not_svn:
            self.inputs = self._compute_files(inputs)
        else:
            self.file += "svn"
            self.md5 = svn_version
            self.getsize = lambda file: 0

    def _compute_files(self, files):
        for file in files:
            if os.path.isdir(file):
                files.remove(file)
                files.extend(list_all_files(file))
        return files

    def _load(self):
        if(os.path.exists(self.file)):
            with open(self.file, 'r', encoding='utf-8') as f:
                kv = json.load(f)
                return kv
        return {}

    # 在脚本执行完之后调用,重新设置缓存信息

    def resave(self):
        kv = {}
        for file in self.inputs:
            if os.path.exists(file):
                kv[file] = {"md5": self.md5(file), "size": self.getsize(file)}
        for file in self.outputs:
            if os.path.exists(file):
                kv[file] = {"md5": md5(file), "size": os.path.getsize(file)}
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(kv, f)

    # 在调用脚本之前调用,用户判断对应的源文件和目标文件是否完全无变更
    def check_changed(self):
        kv = self._load()
        for file in self.inputs:
            if (file not in kv) or (not os.path.exists(file)) or self.getsize(file) != kv[file]["size"] or self.md5(file) != kv[file]["md5"]:
                return True
        for file in self.outputs:
            if (file not in kv) or (not os.path.exists(file)) or os.path.getsize(file) != kv[file]["size"] or md5(file) != kv[file]["md5"]:
                return True
        return False


def __sample():
    call('dir "program files"', "c:")
    print(md5(r"c:\windows\notepad.exe"))

    ck = CheckChange([r"D:\svn"], [], __file__, False)
    if(ck.check_changed()):
        ck.resave()
        print("save!!!")
    else:
        print("not change!!")
