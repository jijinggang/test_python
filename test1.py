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
    import os
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


# test_turtle()
# test_os()
# test_file()
# test_httpServer()
# 需要先安装requests库
# test_requests()
# test_str()
# test_time()
# test_args()
