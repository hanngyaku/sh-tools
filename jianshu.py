# coding=utf-8
# modify by cgg
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def test_selenium():
    url = 'https://mangacross.jp/comics/yabai/132'
    driver = webdriver.ChromiumEdge()
    driver.get(url)

    html = driver.page_source

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
    for i in range(page_num):
        ActionChains(driver).drag_and_drop_by_offset(slider, -move_step * i, 0).pause(1).release().perform()
        html = driver.page_source
        parse_html(html)

    ActionChains(driver).drag_and_drop_by_offset(slider, -200, 0).release().perform()

    html = driver.page_source
    # print(html)
    parse_html(html)
    # time.sleep(10000)
    driver.quit()

def parse_html(contents):
    soup = BeautifulSoup(contents, 'html.parser')

    root = soup.html
    root_childs = [e for e in root.img]
    print(root_childs)

    for item in soup.findAll(class_="comic__pageContent"):
        item_str = item.__str__()

        pattern = '(https://.+\.jpg)'
        result1 = re.search(pattern, item_str)
        if result1:
            print(result1.group())

    # with open("comic.html", "r", encoding='UTF-8') as f:
    #
    #     contents = f.read()
    #
    #     soup = BeautifulSoup(contents, 'html.parser')
    #
    #     root = soup.html
    #     root_childs = [e for e in root.img]
    #     print(root_childs)
    #
    #     for item in soup.findAll(class_="comic__pageContent"):
    #         item_str = item.__str__()
    #
    #         pattern = '(https://.+\.jpg)'
    #         result1 = re.search(pattern, item_str)
    #         if result1:
    #             print(result1.group())
    #
    #     # print(root.body.div.div.div.sectionf)


test_selenium()
