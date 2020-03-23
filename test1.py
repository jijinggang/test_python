def test_turtle():
    import turtle
    turtle.bgcolor(0, 1, 1)
    t = turtle.Turtle()
    t.speed(100)
    for x in range(100):
        t.forward(x)
        t.left(90)


def test_requests():
    import requests
    res = requests.get("http://baidu.com/index.html")
    print(res.text)


def test_httpServer():
    import http
    PORT = 80
    handler = http.server.SimpleHTTPRequestHandler
    httpd = http.server.HTTPServer(("", PORT), handler)
    print("start httpd on ", PORT)
    httpd.serve_forever()


def test_os():
    import os
    print(os.listdir("c:/"))
    print(os.getcwd())


def test_file():
    with open("1.txt", 'a+') as f:
        f.write("hello world")
    with open("1.txt", 'r') as f:
        print(f.read())
    os.remove("1.txt")


def test_str():
    name = "xyz"
    name = f"aaa {name} bbb"
    print(name)
    print(str.upper(name))
    print(str.capitalize(name))


def test_time():
    import time
    print(time.time())
    time.sleep(2)
    print(time.time())
    print(time.localtime())
    print(time.asctime(time.localtime()))


def test_args():
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument("--root", type=str,
                       help="your http file root", default='.')
    parse.add_argument("--port", type=int, help="http socket port", default=80)
    args = parse.parse_args()
    print(args.root, args.port)


def test_process():
    import os
    os.system("ping baidu.com")
    print("1")
    import subprocess
    proc = subprocess.Popen(["ping", "baidu.com"], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    print(out.decode('gb2312'))
    print(err)


def test_collections():
    print("list:")
    l = []
    for i in range(1, 10):
        l.append(i)
    for i in l:
        print(i)

    print("collections:")
    import collections
    a = collections.deque()
    for i in range(1, 10):
        a.append(i)
    while(len(a) > 0):
        print(a.pop())
    pass


def test_except():
    while True:
        n = input("input an integer:")
        try:
            n = int(n)
            break
        except ValueError:
            print("input error, re-input.")
    print(n)


# test_turtle()
# test_os()
# test_file()
# test_httpServer()
# 需要先安装requests库
# test_requests()
# test_str()
# test_time()
# test_args()
# test_process()
# test_collections()
# test_except()
