import http.server
import os.path
import shutil
import mimetypes
import urllib.parse
from http import HTTPStatus
ROOT = ""
HANDLES = {}


class _MyHttpdHandler(http.server.BaseHTTPRequestHandler):

    def _do_get_filelist(self, path):
        files = os.listdir(path)
        td_html = ""
        for file in files:
            if(os.path.isdir(path+"/"+file)):
                file += "/"
            td_html += f'<tr><td><a href="{file}">{file}</a></td></tr>'
        html = f"""<html><head><meta charset="utf-8"></head><body><table>{td_html}</table><body></html>"""
        self.wfile.write(html.encode())

    def _do_get_file(self, path):
        #print("path:", path)
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
        path = root + urllib.parse.unquote(self.path)
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
    import re
    content = None
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r"^---[-]*$", re.MULTILINE)
    result = re.search(pattern, content)
    if(result == None):
        # base markdown
        md = markdown.markdown(content)
        html = f'<html><head><meta charset="utf-8"></head><body>{md}</body></html>'
        wfile.write(html.encode())
    else:
        # slide
        import landslide.generator
        print("THEMES:", landslide.generator.THEMES_DIR)
        ls = landslide.generator.Generator(
            source=path, direct=True, embed=True,)
        html = ls.render()
        wfile.write(html.encode())


def main():
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("--root", type=str,
                       help="your http file root", default='.')
    parse.add_argument("--port", type=int, help="http socket port", default=80)
    args = parse.parse_args()

    reg_ext_handler(".md", _md_handler)
    start(args.root, args.port)


if __name__ == '__main__':
    main()

"""
pyinstaller -F -c --add-binary "C:\Program Files\Python\Python37\Lib\site-packages\landslide\themes;landslide\themes" --hidden-import="pkg_resources.py2_warn" .\test_http.py
"""
