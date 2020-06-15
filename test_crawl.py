import requests_html as rh
import requests
import os
import hashlib
import time
import sys

session = rh.HTMLSession()
urls = set()


def download(url):
    if(url in urls):
        return
    urls.add(url)
    print("download:", url)
    content = requests.get(url).content
    md5 = hashlib.md5()
    md5.update(content)
    name = '../.down/' + md5.hexdigest() + ".gf"
    if(os.path.exists(name)):
        print("skip")
        return
    with open(name, 'wb') as f:
        f.write(content)


def _down_images_by_title(title_link):
    link = title_link
    while link is not None:
        print("next title:", link)
        session = rh.HTMLSession()
        time.sleep(1)
        try:
            h = session.get(link).html
        except Exception as err:
            print(err, "Sleep 1 and retry...")
            time.sleep(1)
            continue

        for img in h.find("img.size-medium"):
            download(img.attrs['src'])
        link = None
        elems = h.find('div.page-links>a:last-child')
        if(elems is not None and len(elems) > 0):
            elem = elems[0]
            if(elem.text == "下一页"):
                link = elem.attrs['href']


def _deal_with_current(r):
    for a in r.html.find('a.title'):
        for link in a.links:
            _down_images_by_title(link)


def _get_next_page(r):
    elems = r.html.find("div#pagenavi>#pagenavi>a:last-child")
    if(elems is not None and len(elems) > 0):
        elem = elems[0]
        if elem.text == "下一页":
            return elem.attrs['href']
    return None


def main(start_url):
    url = start_url
    print("start crawl:", url)
    while True:
        try:
            # session = rh.HTMLSession()
            r = session.get(url)
            _deal_with_current(r)
            url = _get_next_page(r)
            print("next page:", url)

            if url is None:
                break
        # except requests.exceptions.ConnectionError:
        #     print('ConnectionError -- please wait 3 seconds')
        #     time.sleep(3)
        # except requests.exceptions.ChunkedEncodingError:
        #     print('ChunkedEncodingError -- please wait 3 seconds')
        #     time.sleep(3)
        except Exception as err:
            print(err)
            time.sleep(3)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_url = sys.argv[1]
        main(start_url)
    else:
        print("argv error")
