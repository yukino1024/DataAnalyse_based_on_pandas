#encoding:utf-8
import pandas as pd
import numpy as np
import os
from copy import deepcopy


def ReadData(): #读取数据
    total_data = {}
    for year in range(2020,2024):
        year_data = []
        for month in range(1,13):
            if month < 10:
                filename = 'Data/' + str(year) + '/' + str(year) + '0' + str(month) + '.csv'
            else:
                filename = 'Data/' + str(year) + '/' + str(year) + str(month) + '.csv'
            if os.path.exists(filename):
                data = pd.read_csv(filename,encoding='utf-8')
                year_data.append(data)
        total_data[year] = year_data #这里数据按月存储(列表索引=月份-1)
    return total_data


def aggregatedata(data): #聚合数据（来自ReadData函数）
    new_data = deepcopy(data)  #不将原数据改变
    for year in range(2020,2024):
        new_data[year] = pd.concat(new_data[year],ignore_index=True)
    return new_data #这里数据按年存储


def MakeExcel(aggregate_data):  #将数据写入Excel
    try:
        with pd.ExcelWriter('2020年到2023年青岛天气数据.xlsx') as writer:
            for year in range(2020,2024):
                aggregate_data[year].to_excel(writer,index=False,sheet_name=str(year))
    except:
        pass


class Data():   #创建数据类方便后续获取数据
    def __init__(self,month_data,year_data):
        self.month_data = deepcopy(month_data)
        self.year_data = deepcopy(year_data)
        self.original_month_data = deepcopy(month_data)
        self.original_year_data = deepcopy(year_data)
        self.betterdata()
        self.change_index()
        self.check_na()

    def get(self,year,month=0):   #获取月或年数据(分析时使用)
        if month == 0:
            return self.year_data[year]
        else:
            return self.month_data[year][month-1]

    def get_original(self,year,month=0):   #获取原始月或年数据(存入数据库)
        if month == 0:
            return self.original_year_data[year]
        else:
            return self.original_month_data[year][month-1]

    def change_index(self):  #修改索引
        for year in range(2020,2024):
            for i in range(len(self.month_data[year])):
                self.month_data[year][i].set_index('日期',inplace=True)
        for year in range(2020,2024):
            self.year_data[year].set_index('日期',inplace=True)

    def betterdata(self):   #变换形式，方便后续分析(去掉天气单位，增加平均气温，分割天气状况和风力风向)
        for year in range(2020,2024):
                self.year_data[year]['最低气温/最高气温'] = self.year_data[year]['最低气温/最高气温'].str.replace('℃','')
                temp = self.year_data[year]['最低气温/最高气温'].str.split('/',expand=True)
                weather = self.year_data[year]['天气状况'].str.split('/',expand=True)
                wind = self.year_data[year]['风力风向(夜间/白天)'].str.split('/',expand=True)
                temp.columns = ['最低气温','最高气温']
                temp['最低气温'] = temp['最低气温'].astype('int')
                temp['最高气温'] = temp['最高气温'].astype('int')
                temp['平均气温'] = (temp['最高气温'] + temp['最低气温']) / 2
                weather.columns = ['白天天气','夜间天气']
                wind.columns = ['夜间风力风向','白天风力风向']
                self.year_data[year].drop('最低气温/最高气温',axis=1,inplace=True)
                self.year_data[year].drop('天气状况',axis=1,inplace=True)
                self.year_data[year].drop('风力风向(夜间/白天)',axis=1,inplace=True)
                self.year_data[year] = pd.concat([self.year_data[year],weather,temp,wind],axis=1)
        for year in range(2020,2024):
            for i in range(len(self.month_data[year])):
                self.month_data[year][i]['最低气温/最高气温'] = self.month_data[year][i]['最低气温/最高气温'].str.replace('℃','')
                temp = self.month_data[year][i]['最低气温/最高气温'].str.split('/',expand=True)
                weather = self.month_data[year][i]['天气状况'].str.split('/',expand=True)
                wind = self.month_data[year][i]['风力风向(夜间/白天)'].str.split('/',expand=True)
                temp.columns = ['最低气温','最高气温']
                temp['最低气温'] = temp['最低气温'].astype('int')
                temp['最高气温'] = temp['最高气温'].astype('int')
                temp['平均气温'] = (temp['最高气温'] + temp['最低气温']) / 2
                weather.columns = ['白天天气','夜间天气']
                wind.columns = ['夜间风力风向','白天风力风向']
                self.month_data[year][i].drop('最低气温/最高气温',axis=1,inplace=True)
                self.month_data[year][i].drop('天气状况',axis=1,inplace=True)
                self.month_data[year][i].drop('风力风向(夜间/白天)',axis=1,inplace=True)
                self.month_data[year][i] = pd.concat([self.month_data[year][i],weather,temp,wind],axis=1)

    def check_na(self):    #缺失值处理(数值用平均值填充，其他类型用前一列或后一列的值填充)
        for year in range(2020,2024):
            for index in self.year_data[year].columns:
                if self.year_data[year][index].isnull().sum() > 0:
                    if self.year_data[year][index].dtype == int or self.year_data[year][index].dtype == float:
                        self.year_data[year][index].fillna(self.year_data[year][index].mean(),inplace=True)
                    else:
                        bool_index = self.year_data[year][index].isnull()
                        index = np.where(bool_index)[0]
                        try:
                            self.year_data[year].iloc[index,0] = self.year_data[year].iloc[index+1,0]
                        except:
                            self.year_data[year].iloc[index,0] = self.year_data[year].iloc[index-1,0]
            for month in range(0,12):
                for index in self.month_data[year][month].columns:
                    if self.month_data[year][month][index].isnull().sum() > 0:
                        if self.month_data[year][month][index].dtype == int or self.month_data[year][month][index].dtype == float:
                            self.month_data[year][month][index].fillna(self.month_data[year][month][index].mean(),inplace=True)
                        else:
                            bool_index = self.month_data[year][month][index].isnull()
                            index = np.where(bool_index)[0]
                            try:
                                self.month_data[year][month].iloc[index,0] = self.month_data[year][month].iloc[index+1,0]
                            except:
                                self.month_data[year][month].iloc[index,0] = self.month_data[year][month].iloc[index-1,0]


total_data = ReadData()
aggregate_data = aggregatedata(total_data)
MakeExcel(aggregate_data)
data = Data(total_data,aggregate_data)