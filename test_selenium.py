'''
1. pip install selenium
2. 下载chromedriver, 从 http://npm.taobao.org/mirrors/chromedriver/ 找对应自己chrome的版本
'''


def search(key):
    from selenium import webdriver
    driver = webdriver.Chrome("d:/chromedriver.exe")
    driver.get("https://baidu.com")
    elem = driver.find_element_by_id('kw')
    elem.send_keys(key)
    su = driver.find_element_by_id('su')
    su.click()
