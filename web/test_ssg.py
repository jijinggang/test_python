# 静态站点生成
from playwright.sync_api import sync_playwright

def write_file(file, content):
    with open(file, 'wb') as f:
        f.write(content)

def crawl1():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://10.1.8.123/")
        write_file("_page.html", page.content().encode('utf-8'))
        browser.close()



import scrapy
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://baidu.com/',
    ]

    def parse(self, response):
        print("......", response.url)
        #for a in response.css('a'):
        #    yield {
        #        #'author': a.xpath('span/small/text()').get(),
        #        'text': a.attrib['href'],
        #    }

        next_page = response.css('a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)