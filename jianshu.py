# coding=utf-8
import os
import re
import json
import requests
from bs4 import BeautifulSoup
from xvfbwrapper import Xvfb
from os import path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def make_selenium():
    options = Options()
    # options.add_argument('--headless') --无界面模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--incognito")
    options.add_argument("--disable-site-isolation-trials")

    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

class Mangacross:
    # url = 'https://mangacross.jp/comics/yabai/132'
    def __init__(self, comic_name):
        self.comic_name = comic_name
        self.url_base = 'https://mangacross.jp'
        self.url_comic = '{}/comics/{}'.format(self.url_base, self.comic_name)
        # self.save_dir_base = '/Users/cgg/Desktop/img'
        self.save_dir_base = 'comic/img'
        if not path.exists(self.save_dir_base):
            os.makedirs(self.save_dir_base)

    def start_selenium(self):
        display = Xvfb(width=1920, height=1080)
        display.start()
        # try:
        #     dic_episode = self.get_episode_info()
        #     for episode, url in dic_episode.items():
        #         if self.shoud_selenium(episode):
        #             self.selenium(episode, url)
        # except BaseException as e:
        #     print("errorinfo:", e)
        # else:
        #     pass

        dic_episode = self.get_episode_info()
        for episode, url in dic_episode.items():
            if self.shoud_selenium(episode):
                self.selenium(episode, url)

        display.stop()
    def shoud_selenium(self, episode):
        save_dir = '{}/{}/{}'.format(self.save_dir_base, self.comic_name, episode)
        if path.exists(save_dir):
            return False
        return True

    def get_episode_info(self):
        """
        解析主页的内容，查看当前更新的集数
        :return:
        """
        driver = make_selenium()
        driver.get(self.url_comic)
        driver.maximize_window()
        # # 向下滚动200个像素
        # driver.execute_script('window.scrollBy(0,600)')
        # time.sleep(6)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "copy_target_url")))

        html = driver.page_source
        driver.quit()

        with open('test2.html', 'w', encoding='utf-8') as f:
            f.write(html)

        dic_episode = dict()
        self.parse_home_page_html(html, dic_episode)
        print(json.dumps(dic_episode, indent=4, ensure_ascii=False))
        # print(html)
        print("end")
        return dic_episode

    def selenium(self, episode, url):
        """
        使用selenium通过滑动Slider，获取漫画信息
        :return:
        """
        url_episode = '{}{}'.format(self.url_base, url)
        print('start selenium: {}'.format(url_episode))

        driver = make_selenium()
        driver.get(url_episode)
        driver.maximize_window()

        # 空格要变为.才行
        above = driver.find_element(By.CLASS_NAME,
                                    'viewer-page__button.viewer-page__button--green.viewer-page__button--large.viewer'
                                    '-page__button--read')
        above.click()
        # 分析页数出来
        slider = driver.find_element(By.CLASS_NAME,
                                     "controller__slider_bar")
        page_num = 10
        move_step = 100 / page_num
        dir_img = {}
        for i in range(page_num):
            ActionChains(driver).drag_and_drop_by_offset(slider, -move_step * i, 0).pause(1).release().perform()
            html = driver.page_source
            self.parse_html(html, dir_img)

        ActionChains(driver).drag_and_drop_by_offset(slider, -200, 0).release().perform()

        print(json.dumps(dir_img, indent=4, ensure_ascii=False))
        self.download_img(dir_img, self.comic_name, episode)
        driver.quit()

    def parse_html(self, contents, dir_img):
        """
        解析漫画网页信息，把漫画的页数信息爬取下来，并且记录
        :param contents:网页内容
        :param dir_img:页数-url字典
        :return:
        """
        soup = BeautifulSoup(contents, 'html.parser')

        for item in soup.findAll(class_="comic__page"):
            item_str = item.__str__()
            page_index = item['data-page-index']
            pattern = '(https://.+\.jpg)'
            result1 = re.search(pattern, item_str)
            if result1:
                # print('page = {}, url = {}'.format(page_index, result1.group()))
                dir_img[page_index] = result1.group()

    def parse_home_page_html(self, content, dir_episode):
        soup = BeautifulSoup(content, 'html.parser')
        for item in soup.findAll(class_="episode-list__item"):
            for child in item.children:
                href = child['href']
                if href:
                    # print(href)
                    base_name = path.basename(href)
                    # print(base_name)
                    dir_episode[base_name] = href

    def download_img(self, img_dir, comic_name, episode):
        save_dir = '{}/{}/{}'.format(self.save_dir_base, comic_name, episode)
        if not path.exists(save_dir):
            os.makedirs(save_dir)

        for key, value in img_dir.items():
            file_name = '{}/{}.jpg'.format(save_dir, key)
            if path.exists(file_name):
                continue

            r = requests.get(value)
            print(file_name)
            with open(file_name, 'wb') as f:
                f.write(r.content)

# test_selenium()
def parse_html_local():
    with open("test.html", "r", encoding='UTF-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        for item in soup.findAll(class_="episode-list__item"):
            for child in item.children:
                href = child['href']
                if href:
                    print(href)
                    base_name = path.basename(href)
                    print(base_name)
                    # episode_number = child.find(class_ = 'episode-list__number')
                    # if episode_number:
                    #     print(episode_number.string)

            # page_index = item['data-page-index']
            # pattern = '(https://.+\.jpg)'
            # result1 = re.search(pattern, item_str)
            # if result1:
            #     print('page = {}, url = {}'.format(page_index, result1.group()))

def test():
    url = 'https://mangacross.jp/images/episode_page/CB1FOYOEsirt3WYZSk-RSNf1V-EIUmiQ3QhdP9P2glI/image/pc.jpg'
    r = requests.get(url)
    print(len(r.content))
mangacross = Mangacross(comic_name='yabai')
mangacross.start_selenium()
# parse_html_local()
# test()
