# coding=utf-8

from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from os import path
import json
class Mangacross:
    # url = 'https://mangacross.jp/comics/yabai/132'
    def __init__(self, comic_name, comic_episode):
        self.comic_name = comic_name
        self.comic_episode = comic_episode
        self.url_base = 'https://mangacross.jp'
        self.url_comic = 'https://mangacross.jp/comics/{}'.format(self.comic_name)
        self.url_episode = 'https://mangacross.jp/comics/{}/{}'.format(self.comic_name, self.comic_episode)
    def get_episode_info(self):
        driver = webdriver.ChromiumEdge()
        driver.get(self.url_comic)
        driver.maximize_window()
        # 向下滚动200个像素
        driver.execute_script('window.scrollBy(0,600)')
        time.sleep(6)
        html = driver.page_source
        dic_episode = dict()
        self.parse_home_page_html(html, dic_episode)
        print(json.dumps(dic_episode, indent=4, ensure_ascii=False))
        # print(html)
    def selenium(self):
        """
        使用selenium通过滑动Slider，获取漫画信息
        :return:
        """

        driver = webdriver.ChromiumEdge()
        driver.get(self.url)

        driver.maximize_window()

        # 空格要变为.才行
        above = driver.find_element(By.CLASS_NAME,
                                    'viewer-page__button.viewer-page__button--green.viewer-page__button--large.viewer'
                                    '-page__button--read')
        above.click()
        time.sleep(1)
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


mangacross = Mangacross(comic_name='yabai', comic_episode='132')
mangacross.get_episode_info()
# parse_html_local()