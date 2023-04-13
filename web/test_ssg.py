from playwright.sync_api import sync_playwright

def write_file(file, content):
    with open(file, 'wb') as f:
        f.write(content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://10.1.8.123/")
    write_file("_page.html", page.content().encode('utf-8'))
    browser.close()