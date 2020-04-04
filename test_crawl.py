import requests_html as rh
import requests
import os
import hashlib
import time
import sys

session = rh.HTMLSession()

urls = set()


def download(url):
    print(url)
    return
    if(url in urls):
        return
    time.sleep(0.2)
    urls.add(url)
    print("download:", url)
    content = requests.get(url).content
    md5 = hashlib.md5()
    md5.update(content)
    name = '../.down/'+md5.hexdigest()+".gf"
    if(os.path.exists(name)):
        print("skip")
        return
    with open(name, 'wb') as f:
        f.write(content)


def _down_images_by_title(title_link):
    link = title_link
    while link is not None:

        h = session.get(link).html
        for img in h.find("img.size-medium"):
            download(img.attrs['src'])
        elems = h.find('div.page-links>a:last-child')
        if(elems is None or len(elems) < 1):
            link = None
        else:
            link = elems[0].attrs['href']


def _deal_with_current(r):
    print("-----new page-----")
    for a in r.html.find('a.title'):
        for link in a.links:
            _down_images_by_title(link)


def _get_next_page(r):
    elems = r.html.find("div#pagenavi>#pagenavi>a:last-child")
    if(elems is None or len(elems) < 1):
        return None
    return elems[0].attrs['href']


def main(start_url):
    url = start_url
    print("start crawl:", url)
    while True:
        try:
            #session = rh.HTMLSession()
            r = session.get(url)
            _deal_with_current(r)
            url = _get_next_page(r)
            if url is None:
                break
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except:
            print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        main(start_url)
    else:
        print("argv error")
