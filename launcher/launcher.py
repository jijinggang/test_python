import io
import tkinter as tk
from tkinter.constants import END
import tkinter.ttk as ttk
import time
import requests
import os
import util
from contextlib import closing
from enum import Enum
from threading import Thread
import tkinter.messagebox as msgbox


def get_start_path():
    import sys
    import os
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return bundle_dir


class Event(Enum):
    START = 1
    UPDATE = 2
    END = 3


# 登陆器界面
class Launcher:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Launcher")
        # self.win.geometry('1280x720')
        util.center_window(self.win, 1280, 720)
        self.init_image()
        self.init_progress()

        button = tk.Button(self.win, text='Running', command=self.show)
        button.place(x=950, y=680)
        self.init_updater()
        self.win.mainloop()

    def init_progress(self):
        self.progress = ttk.Progressbar(self.win)
        self.progress.place(x=100, y=700, width=800, height=5)
        # 进度值最大值
        self.progress['maximum'] = 100
        # 进度值初始值
        self.progress['value'] = 0

    def init_image(self):
        import os.path
        start_path = get_start_path()
        print(start_path)
        self.photo = tk.PhotoImage(file=os.path.join(
            start_path, 'bk.png'))
        self.image = tk.Canvas(
            self.win, width=self.photo.width(), height=self.photo.height())
        self.image.pack()
        self.image.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def show(self):
        pass
        # for i in range(100):
        #     # 每次更新加1
        #     self.progress['value'] = i + 1
        #     # 更新画面
        #     self.win.update()
        #     time.sleep(0.05)

    def callback(self, evt: Event, value):
        if evt == Event.START:
            self.progress['maximum'] = value
        elif evt == Event.UPDATE:
            self.progress['value'] += value
        elif evt == Event.END:
            msgbox.showinfo("", 'update completed!')
            pass

    def init_updater(self):
        self.updater = Updater(self.callback)
        self.updater.start()


# 文件下载


class Updater(Thread):
    def __init__(self, callback):
        Thread.__init__(self)
        self.callback = callback

    def run(self):
        url = "http://localhost/"
        txt = self.download_filelist(url+"filelist.txt")
        lines = self.parse_filelist(txt)
        if not lines:
            raise Exception("parse error")
            pass
        downfiles = []
        downsize = 0
        for file, size, md5 in lines:
            local = os.getcwd() + '\\.app\\'+file
            util.ensure_dir(local)
            remote = url+md5+".bin"
            if self.check_diff(local, size, md5):
                downfiles.append((local, remote))
                downsize += size
        self.callback(Event.START, downsize)
        for local, remote in downfiles:
            self.download_file(remote, local)
        self.callback(Event.END, 0)
    # 下载一个大文件

    def download_file(self, remote, local):
        with closing(requests.get(url=remote, verify=False, stream=True, timeout=5)) as res:
            with open(local, 'wb+') as fd:
                print('download:', remote, local)
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        fd.write(chunk)
                        self.callback(Event.UPDATE, len(chunk))
    # 检查文件是否跟服务器相同

    def check_diff(self, local, size, md5):
        if not os.path.exists(local):
            return True
        if os.path.getsize(local) != size:
            return True
        return util.get_md5(local) != md5
    # 下载filelist.txt

    def download_filelist(self, url):
        res = requests.get(url)
        return res.text

    def parse_filelist(self, txt):
        buf = io.StringIO(txt)
        lines = buf.readlines()
        infos = []
        for line in lines:
            line = line.strip('\r\n')
            lineinfos = str.split(line, ':')
            if len(lineinfos) != 3:
                return None
            else:
                infos.append((lineinfos[0], int(lineinfos[1]), lineinfos[2]))
        return infos


Launcher()
# Updater().start()

# pyinstaller -F -w --add-data "bk.png;." --add-data "config.conf" launcher.py
