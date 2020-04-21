import http.server
import urllib
import os.path
import shutil

ROOT = '.'


def get_file_list(path):
    files = os.listdir(path)
    td_html = ""
    for file in files:
        if(os.path.isdir(path+"/"+file)):
            file += "/"
        td_html += f'<tr><td><a href="{file}">{file}</a></td></tr>'
    return f"""<html><body><table>{td_html}</table><body></html>"""


def write_file_content(w, path):
    with open(path, 'r') as f:
        w.write(f.read())
    pass


class MyHttpHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        root = ROOT.replace('\\', '/')
        path = root + self.path
        print(path)
        if(os.path.isdir(path)):
            html = get_file_list(path).encode('utf8')
            self.wfile.write(html)
            return
        if(os.path.isfile(path)):
            with open(path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
            return

    def do_POST(self):
        pass


class Httpd:
    def __init__(self, root=".", port=80):
        self._root = root
        self._port = port

    def start(self):
        handler = MyHttpHandler
        server = http.server.HTTPServer(('', self._port), handler)
        server.serve_forever()


Httpd().start()
