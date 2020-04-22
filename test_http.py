import http.server
import os.path
import shutil
import mimetypes
from http import HTTPStatus
ROOT = ""
HANDLES = {}

http.server.SimpleHTTPRequestHandler


def format_text_plain(text: str):
    return f'<html><head><head><meta charset="utf-8"></head></head><body>{text}</body></html>'


class _MyHttpdHandler(http.server.BaseHTTPRequestHandler):

    def _do_get_filelist(self, path):
        files = os.listdir(path)
        td_html = ""
        for file in files:
            if(os.path.isdir(path+"/"+file)):
                file += "/"
            td_html += f'<tr><td><a href="{file}">{file}</a></td></tr>'
        html = f"""<html><body><table>{td_html}</table><body></html>"""
        self.wfile.write(html.encode())

    def _do_get_file(self, path):
        mime = mimetypes.guess_type(path)[0]
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", f"{mime}; charset=utf-8")
        self.end_headers()
        ext = os.path.splitext(path)[1]
        func = HANDLES.get(ext.lower())
        if func:
            func(path, self.wfile)
        else:
            # default
            with open(path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)

    def do_GET(self):
        root = ROOT.replace('\\', '/')
        path = root + self.path
        if(os.path.isdir(path)):
            self._do_get_filelist(path)
        else:
            self._do_get_file(path)

    def do_POST(self):
        pass


def reg_ext_handler(ext, ext_handler_func):
    HANDLES[ext] = ext_handler_func


def start(root=".", port=80):
    global ROOT
    ROOT = root
    print("start httpd", root, port)
    server = http.server.HTTPServer(('', port), _MyHttpdHandler)
    server.serve_forever()


def _md_handler(path, wfile):
    import markdown
    with open(path, 'r', encoding='utf-8') as f:
        md = markdown.markdown(f.read())
        html = format_text_plain(md)
        wfile.write(html.encode())


reg_ext_handler(".md", _md_handler)
start()
