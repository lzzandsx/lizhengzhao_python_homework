from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import datetime
from pymongo import MongoClient
import re

def main():
    #因为公众号的url会变化，所以利用他上一层的网页来获取
    base_url = 'https://weixin.sogou.com/weixin?type=1&query=it之家'
    patten = '.txt-box .tit a'
    addr = webdrive(base_url,patten)[0]
    get_page(addr.get_attribute('href'))#it之家的url

def get_page(url):
    #获取公众号里面的内容
    patten = '.weui_msg_card h4'
    browser = webdriver.Chrome()
    browser.get(url)
    addrs  = browser.find_elements_by_css_selector(patten)
    date_origin = browser.find_elements_by_css_selector('.weui_media_extra_info')
    i=0
    #推文的url
    for addr in addrs:
        base_url = 'https://mp.weixin.qq.com'
        target_addr = base_url+addr.get_attribute('hrefs')
        date = date_origin[i].text
        get_html(target_addr,date)

def get_html(addr,date):
    #获取推文网页里面的内容，字典格式
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    }
    dict = {}
    response = requests.get(addr,headers=header)
    response.encoding = 'utf-8'
    html = response.text
    doc = BeautifulSoup(html,'lxml')
    title = doc.title.string
    article = doc.select('.rich_media_content')[0].get_text()
    dict['title'] = title
    dict['content'] = article
    dict['url'] = addr
    dict['date'] = date
    write_in_database(dict)



def write_in_database(dict):
    #启动数据库，在本文章没有存入的情况下存入
    client = MongoClient('mongodb://localhost:27017/')
    database = client.IThome
    collection = database.articles
    dict['Id'] = collection.find().count()
    print(dict)
    if collection.find_one({'title':dict['title']}) == None:
        collection.insert(dict)


def webdrive(url,patten):
    browser = webdriver.Chrome()
    browser.get(url)
    return browser.find_elements_by_css_selector(patten)


if __name__ == '__main__':
    #这个是定时启动
    while True:
        now = datetime.datetime.now()
        if (now.hour == 9 or now.hour == 21) and now.second == 0:
            main()
        time.sleep(60)

