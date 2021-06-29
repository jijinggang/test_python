# test_python
python test code

## 开发环境
- Python3.8+
- VSCode
- VSCode插件:Python/Pylance
- Python插件选项中,打开Flake8 Enabled 并且最好增加 Flake8 Args "--ignore=E50"来忽略单行长度80的检查
- 部分非标准库需要用pip install安装

## 离线安装
1. 下载一个Python嵌入版,例如[Python3.7.7](https://www.python.org/ftp/python/3.7.7/python-3.7.7-embed-amd64.zip)
2. 下载[get-pip.py](https://bootstrap.pypa.io/get-pip.py)
3. 用解压目录的python.exe执行get-pip.py
4. 修改解压目录下的python37._pth, 把import site注释打开
5. 用解压目录的Scripts\pip安装其他包
6. 拷贝整个python目录即可


## 打包
### pyinstaller
使用pyinstaller
```
    pyinstaller -F -c 1.py
```
参数说明:
- -F/-D 打包成一个完整文件/分散多个文件
- -w/-c 打包成窗口/控制台程序
- --add-binary/--add-data 非python代码的其他运行时直接使用的文件,可以指定文件或目录
### 打包异常情况处理
如果出现No module named ‘pkg_resources.py2_warn’错误,可以加入--hidden-import命令行参数.

```
pyinstaller -F -c --add-binary "C:\Program Files\Python\Python37\Lib\site-packages\landslide\themes;landslide\themes" --hidden-import="pkg_resources.py2_warn" .\test_http.py
```

## 使用ipython作为shell程序
把ipython脚本存成1.ipy文件,如
```
curdir = %pwd
%pushd ..
files = !dir /b
for f in files:
  print(f)
%popd
```
然后运行
```
python -m IPython 1.ipy
```
常用ipython指令
- %magic 显示特殊指令帮助
- %cd 切换目录
- %pushd %popd 改变当前目录
- %pwd 显示当前目录
- %run 运行一个python文件
- %set_env 设置环境变量

## 更多Python示例代码
<https://github.com/gto76/python-cheatsheet>