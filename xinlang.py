from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import datetime


def get_page(url):
    header = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    }
    html = requests.get(url,headers=header)
    html.encoding  = 'utf-8'
    return html

def parse_page(html,addr):
    #获取网页里面目标信息，以字典的方式储存
    dict = {}
    doc = BeautifulSoup(html,'lxml')
    title = doc.select('h1')
    if len(title)==0:
        return
    articles = doc.select('#artibody p')#得到的是一个列表
    content = ''
    date = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    for article in articles:
        content += article.get_text()
    dict['date'] = date
    dict['title'] = title[0].get_text().strip()
    dict['content'] = content
    dict['url'] = addr.get_attribute('href')
    write_in_database(dict)

def write_in_database(dict):
    #当文章未存入时存入
    client = MongoClient('mongodb://localhost:27017/')
    database = client.xinlang
    collection = database.articles
    dict['Id'] = collection.find().count()
    print(dict)
    if collection.find_one({'title':dict['title']}) == None:
        collection.insert(dict)



def main():
    url = 'https://mobile.sina.com.cn/'
    browser = webdriver.Chrome()
    browser.get(url)
    addrs = browser.find_elements_by_css_selector('#feedCard #feedCardContent .feed-card-item h2 a')
    #获取每篇文章的url
    for addr in addrs:
        html=get_page(addr.get_attribute('href')).text
        parse_page(html,addr)

if __name__ == '__main__':
     while(True):#定时在9点和21点时运行
         now = datetime.datetime.now()
         if (now.hour == 9 or now.hour == 21) and now.minute == 0 :
             main()
         time.sleep(60)

        ##ok

