import http.server
import argparse


def parseArgs():
    parse = argparse.ArgumentParser()
    parse.add_argument("--root", type=str,
                       help="your http file root", default='.')
    parse.add_argument("--port", type=int, help="http socket port", default=80)
    args = parse.parse_args()
    return (args.root, args.port)


def start(root, port):
    print("start httpd", root, port)
    server = http.server.HTTPServer(
        ('', port), http.server.SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    root, port = parseArgs()
    start(root, port)


main()
