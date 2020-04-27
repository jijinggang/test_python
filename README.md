# test_python
python test code

## 安装
- Python3
- VSCode
- Python插件
- kite 插件及 kite 后台服务
- 部分非标准库需要用pip install安装

## 打包
使用pyinstaller
```
    pyinstaller -F -c 1.py
```
参数说明:
- -F/-D 打包成一个完整文件/分散多个文件
- -w/-c 打包成窗口/控制台程序
- --add-binary/--add-data 非python代码的其他运行时直接使用的文件,可以指定文件或目录
## 打包异常情况处理
如果出现No module named ‘pkg_resources.py2_warn’错误,可以加入--hidden-import命令行参数.

```
pyinstaller -F -c --add-binary "C:\Program Files\Python\Python37\Lib\site-packages\landslide\themes;landslide\themes" --hidden-import="pkg_resources.py2_warn" .\test_http.py
```

## 更多Python示例代码
<https://github.com/gto76/python-cheatsheet>