'''
1. pip install selenium
2. 下载chromedriver, 从 http://npm.taobao.org/mirrors/chromedriver/ 找对应自己chrome的版本
'''
import sys
import os
from selenium.common.exceptions import InvalidArgumentException
from fake_useragent import UserAgent
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


class util:
    @staticmethod
    def listdir(dir, *exts):
        dir = dir.replace('\\', '/')
        files = os.listdir(dir)
        results = []
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if len(exts) == 0 or ext in exts:
                results.append(dir+"/"+file)
        return results


class Robot:
    def __init__(self):
        pass

    def start(self):
        driver = None
        opts = webdriver.ChromeOptions()
        opts.add_argument('--disable-infobars')
        # opts.add_argument('--disk-cache-dir=./cache')
        username = os.getlogin()
        opts.add_argument(
            f'--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data')
        try:
            driver = webdriver.Chrome(chrome_options=opts)
            driver.implicitly_wait(20)
        except InvalidArgumentException:
            print("打开Chrome出错, 请先关闭所有Chrome窗口后再重试")
            return False
        self._driver = driver
        return True

    def upload_file(self, file):
        self._driver.get(
            'https://www.youtube.com/upload?redirect_to_creator=true&fr=4&ar=1586851028086&nv=1')
        self._driver.find_element_by_css_selector(
            r'#upload-privacy-selector > .yt-uix-button-content').click()
        self._driver.find_element_by_css_selector(
            r'#body > ul > li:nth-child(2) > span').click()
        self._driver.find_element_by_css_selector(
            r'#upload-prompt-box > div > input').send_keys(file)
        self._driver.find_elements_by_css_selector(
            r'.save-cancel-buttons > .yt-uix-button-primary > .yt-uix-button-content')[0].click()

    def upload_folder(self, folder):
        files = util.listdir(folder)
        for file in files:
            print("开始上传:", file)
            self.upload_file(file)


def main():
    robot = Robot()
    if robot.start():
        robot.upload_folder("d:/_m")
