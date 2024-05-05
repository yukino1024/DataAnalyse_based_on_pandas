#encoding:utf-8
import requests as req
from bs4 import BeautifulSoup as bs
import random
import time
import os
import csv
from fake_useragent import UserAgent
ua = UserAgent()


def crawler():  #执行爬虫并存储数据
    dir()
    for year in range(2023,2019,-1):
        for month in range(1,13):
            head = {
    "User-Agent": ua.random,
    "Connection" : "cloes"
    }
            if month < 10:
                day = str(year) + '0' + str(month)
            else:
                day = str(year) + str(month)
            url = 'http://www.tianqihoubao.com/lishi/qingdao/month/'+ day + '.html'
            print('正在爬取' + str(year) + '年' + str(month) + '月' + '的数据')
            print('数据网址:' + url)
            html = gethtml(url,head)
            print(str(year) + '年' + str(month) + '月' + '的数据爬取完成')
            wr_csv(html,day,year)
    print('数据爬取完成')


def betterdata(data):   #除去数据中的换行、回车、空格，变换日期格式
    data = data.replace('\n','',-1)
    data = data.replace('\r','',-1)
    data = data.replace(' ','',-1)
    data = data.replace('年','-')
    data = data.replace('月','-')
    if data != '日期':
        data = data.replace('日','')
    return data


def gethtml(url,head):  #获取网页源码
    session = req.Session()
    for i in range(5):  #获取失败后重试
        try:
            response = session.get(url, headers=head)
            response.raise_for_status()  
        except req.exceptions.RequestException as e:
            print(f'Request failed: {e}')
            time.sleep(random.uniform(0.5,1.5))  
        else:
            break  
    return response.text


def wr_csv(html,day,year):   #将数据写入csv文件
    csv_name = 'Data/' + str(year) + '/' + day + '.csv'
    with open(csv_name, 'w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        soup = bs(html, 'html.parser')
        table = soup.find('table')
        tr = table.find_all('tr')
        data = []
        for x in tr:
            td = x.find_all('td')
            for y in td:
                data.append(betterdata(y.text.strip()))
            writer.writerow(data)
            data = []


def dir():  #创建文件夹分类数据
    try:
        os.mkdir('Data')
        os.mkdir('Data/2023')
        os.mkdir('Data/2022')
        os.mkdir('Data/2021')
        os.mkdir('Data/2020')
    except:
        pass