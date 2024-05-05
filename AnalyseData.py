#encoding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PertreatData import data   #导入数据类

year_ana = {}
month_ana = {}

def analyse():

    def cut_temp(temp): #温度分段
        if temp<0:
            return '冷' #<0
        elif temp<=15:
            return '凉'   #1-15
        elif temp<=25:
            return '舒适'  #16-25
        elif temp<=35:
            return '热'  #26-35
        else:
            return '非常热'    #>35

    def cut_tempdiff(diff): #温差分段
        if diff<3:
            return '小' #<3
        elif diff<=6:
            return '中'    #4-6
        else:
            return '大' #>6

    def cut_wind(wind): #风力分段
        if wind<=2:
            return '轻风' #<2
        elif wind<=4:
            return '和风'    #3-4
        elif wind<=6:
            return '强风'    #5-6
        elif wind<=8:
            return '大风'    #7-8
        else:
            return '狂风' #>8

    '''
    按年进行分析
    '''
    for year in range(2020,2024):
        year_data = data.get(year)
        year_ana[year] = {
            '白天天气':{},
            '夜间天气':{},
            '温度':{},
            '温差':{},
            '白天风向':{},
            '白天风力':{},
            '夜间风向':{},
            '夜间风力':{},
            '未变天气':0,
            '未变风向':0,
            '零下天数':0,
            '温度总体':'',  #后续会用describe()方法的返回值填充
            '最高温':'',    #元组(最高温,日期)
            '最低温':''     #元组(最低温,日期)
        }
        for index,row in year_data.iterrows():
            #白天天气
            day_weather = row['白天天气']
            if day_weather in year_ana[year]['白天天气']:
                year_ana[year]['白天天气'][day_weather] += 1
            else:
                year_ana[year]['白天天气'][day_weather] = 1
            #夜间天气
            night_weather = row['夜间天气']
            if night_weather in year_ana[year]['夜间天气']:
                year_ana[year]['夜间天气'][night_weather] += 1
            else:
                year_ana[year]['夜间天气'][night_weather] = 1
            if day_weather == night_weather:
                year_ana[year]['未变天气'] += 1
            #温度
            h_temp = row['最高气温']
            l_temp = row['最低气温']
            diff = h_temp - l_temp
            ave_temp = (h_temp + l_temp)/2
            if cut_temp(ave_temp) in year_ana[year]['温度']:
                year_ana[year]['温度'][cut_temp(ave_temp)] += 1
            else:
                year_ana[year]['温度'][cut_temp(ave_temp)] = 1
            #温差
            if cut_tempdiff(diff) in year_ana[year]['温差']:
                year_ana[year]['温差'][cut_tempdiff(diff)] += 1
            else:
                year_ana[year]['温差'][cut_tempdiff(diff)] = 1
            #白天风向风力
            day_wind = row['白天风力风向']
            d_wind = day_wind.find('风') + 1
            d_wind = day_wind[:d_wind]
            strong = day_wind.find('级') - 1
            strong = int(day_wind[strong])
            if d_wind in year_ana[year]['白天风向']:
                year_ana[year]['白天风向'][d_wind] += 1
            else:
                year_ana[year]['白天风向'][d_wind] = 1
            if cut_wind(strong) in year_ana[year]['白天风力']:
                year_ana[year]['白天风力'][cut_wind(strong)] += 1
            else:
                year_ana[year]['白天风力'][cut_wind(strong)] = 1
            #夜间风向风力
            night_wind = row['夜间风力风向']
            n_wind = night_wind.find('风') + 1
            n_wind = night_wind[:n_wind]
            strong = night_wind.find('级') - 1
            strong = int(night_wind[strong])
            if n_wind in year_ana[year]['夜间风向']:
                year_ana[year]['夜间风向'][n_wind] += 1
            else:
                year_ana[year]['夜间风向'][n_wind] = 1
            if cut_wind(strong) in year_ana[year]['夜间风力']:
                year_ana[year]['夜间风力'][cut_wind(strong)] += 1
            else:
                year_ana[year]['夜间风力'][cut_wind(strong)] = 1
            if d_wind == n_wind:
                year_ana[year]['未变风向'] += 1
        #总体分析
        year_ana[year]['温度总体'] = year_data['平均气温'].describe()
        year_ana[year]['最高温'] = (year_data['最高气温'].max(),year_data['最高气温'].idxmax())
        year_ana[year]['最低温'] = (year_data['最低气温'].min(),year_data['最低气温'].idxmin())
        underzero = year_data['最低气温'] < 0 
        year_ana[year]['零下天数'] = underzero.value_counts()[True]

    '''
    按月进行分析
    '''
    for year in range(2020,2024):
        for month in range(1,13):
            month_data = data.get(year,month)
            month_ana[(year,month)] = {
            '白天天气':{},
            '夜间天气':{},
            '零下天数':0,
            '温度总体':'',  #后续会用describe()方法的返回值填充
            '最高温':'',    #元组(最高温,日期)
            '最低温':''     #元组(最低温,日期)
            }
            for index,row in month_data.iterrows():
                #白天天气
                day_weather = row['白天天气']
                if day_weather in month_ana[(year,month)]['白天天气']:
                    month_ana[(year,month)]['白天天气'][day_weather] += 1
                else:
                    month_ana[(year,month)]['白天天气'][day_weather] = 1
                #夜间天气
                night_weather = row['夜间天气']
                if night_weather in month_ana[(year,month)]['夜间天气']:
                    month_ana[(year,month)]['夜间天气'][night_weather] += 1
                else:
                    month_ana[(year,month)]['夜间天气'][night_weather] = 1
            #总体分析
            month_ana[(year,month)]['温度总体'] = month_data['平均气温'].describe()
            month_ana[(year,month)]['最高温'] = (month_data['最高气温'].max(),month_data['最高气温'].idxmax())
            month_ana[(year,month)]['最低温'] = (month_data['最低气温'].min(),month_data['最低气温'].idxmin())
            underzero = month_data['最低气温'] < 0
            try:
                month_ana[(year,month)]['零下天数'] = underzero.value_counts()[True]
            except:
                month_ana[(year,month)]['零下天数'] = 0



def wr_txt():
    mk_dir()
    '''
    年分析
    '''
    for year in range(2020,2024):
        ana_data = year_ana[year]
        stay_weather = ana_data['未变天气']
        tot_weather = ana_data['温度总体']
        high_temp = ana_data['最高温']
        low_temp = ana_data['最低温']
        undet_zero = ana_data['零下天数']
        with open(f'分析结果/年分析/{str(year)}年/分析结果.txt','w',encoding='utf-8') as f:
            f.write(f'-------------------总体温度------------------')
            f.write('\n平均温度：%.2f'%tot_weather['mean'])
            f.write(f'\n%25分位数：{tot_weather["25%"]}')
            f.write(f'\n%50分位数：{tot_weather["50%"]}')
            f.write(f'\n%75分位数：{tot_weather["75%"]}')
            f.write(f'\n最高温度：{high_temp[0]}({high_temp[1]})')
            f.write(f'\n最低温度：{low_temp[0]}({low_temp[1]})')
            f.write(f'\n')
            f.write(f'\n-------------------天气情况------------------')
            f.write(f'\n整日天气未变天数：{stay_weather}')
            f.write(f'\n零下天数：{undet_zero}')


    '''
    月分析
    '''
    for year in range(2020,2024):
        for month in range(1,13):
            ana_data = month_ana[(year,month)]
            tot_weather = ana_data['温度总体']
            high_temp = ana_data['最高温']
            low_temp = ana_data['最低温']
            undet_zero = ana_data['零下天数']
            with open(f'分析结果/月分析/{str(year)}年/{str(year)}年{str(month)}月/分析结果.txt','w',encoding='utf-8') as f:
                f.write(f'-------------------总体温度------------------')
                f.write('\n平均温度：%.2f'%tot_weather['mean'])
                f.write(f'\n%25分位数：{tot_weather["25%"]}')
                f.write(f'\n%50分位数：{tot_weather["50%"]}')
                f.write(f'\n%75分位数：{tot_weather["75%"]}')
                f.write(f'\n最高温度：{high_temp[0]}({high_temp[1]})')
                f.write(f'\n最低温度：{low_temp[0]}({low_temp[1]})')
                f.write(f'\n')
                f.write(f'\n-------------------天气情况------------------')
                f.write(f'\n零下天数：{undet_zero}')


def dr_pic():
    mk_dir()
    '''
    年分析
    '''
    for year in range(2020,2024):
        ana_data = year_ana[year]
        day_weather = ana_data['白天天气']
        night_weather = ana_data['夜间天气']
        temp = ana_data['温度']
        tempdiff = ana_data['温差']
        day_wind = ana_data['白天风向']
        day_windstrong = ana_data['白天风力']

        #天气
        weather_name = []
        day_weather_value = []
        night_weather_value = []
        for key in day_weather:
            weather_name.append(key)
        for key in night_weather:
            if key not in weather_name:
                weather_name.append(key)
        for key in weather_name:
            day_weather_value.append(day_weather.get(key,0))
            night_weather_value.append(night_weather.get(key,0))
        x1 = [i+1 for i in range(len(weather_name))]
        x2 = [i+1.2 for i in range(len(weather_name))]
        plt.figure(figsize=(20,8),dpi=100)
        plt.bar(x1,day_weather_value,width=0.2,label='白天天气',color='r',alpha=0.5)
        plt.bar(x2,night_weather_value,width=0.2,label='夜间天气',color='b',alpha=0.5)
        plt.xlabel('天气')
        plt.ylabel('天数')
        plt.title(f'青岛{str(year)}年天气情况')
        plt.xticks([i+0.1 for i in x1],weather_name)
        plt.yticks(range(0,160,10))
        plt.grid(linestyle='--',alpha=0.5)
        plt.legend()
        plt.savefig(f'分析结果/年分析/{str(year)}年/图/天气情况.png')
        plt.clf()

        #风向
        wind_name = []
        wind_value = []
        for key,value in day_wind.items():
            wind_name.append(key)
            wind_value.append(value)
        x = [i+1 for i in range(len(wind_name))]
        plt.figure(figsize=(20,8),dpi=100)
        plt.bar(x,wind_value,width=0.2,color='b',alpha=0.5)
        plt.xlabel('风向')
        plt.ylabel('天数')
        plt.title(f'青岛{str(year)}年风向情况')
        plt.xticks(x,wind_name)
        plt.yticks(range(0,130,10))
        plt.grid(linestyle='--',alpha=0.5)
        plt.savefig(f'分析结果/年分析/{str(year)}年/图/风向情况.png')
        plt.clf()

        #风力
        winds_name = []
        winds_value = []
        for key,value in day_windstrong.items():
            winds_name.append(key)
            winds_value.append(value)
        plt.figure(figsize=(12,10),dpi=100)
        plt.pie(winds_value,labels=winds_name,autopct='%1.2f%%')
        plt.axis('equal')
        plt.legend()
        plt.title(f'青岛{str(year)}年风力情况')
        plt.savefig(f'分析结果/年分析/{str(year)}年/图/风力情况.png')
        plt.clf()

        #温度
        temp_name = []
        temp_value = []
        for key,value in temp.items():
            temp_name.append(key)
            temp_value.append(value)
        plt.figure(figsize=(12,10),dpi=100)
        plt.pie(temp_value,labels=temp_name,autopct='%1.2f%%')
        plt.axis('equal')
        plt.legend()
        plt.title(f'青岛{str(year)}年温度情况')
        plt.savefig(f'分析结果/年分析/{str(year)}年/图/温度情况.png')
        plt.clf()

        #温差
        tempdiff_name = []
        tempdiff_value = []
        for key,value in tempdiff.items():
            tempdiff_name.append(key)
            tempdiff_value.append(value)
        plt.figure(figsize=(12,10),dpi=100)
        plt.pie(tempdiff_value,labels=tempdiff_name,autopct='%1.2f%%')
        plt.axis('equal')
        plt.legend()
        plt.title(f'青岛{str(year)}年温差情况')
        plt.savefig(f'分析结果/年分析/{str(year)}年/图/温差情况.png')
        plt.clf()


    '''
    月分析
    '''
    for year in range(2020,2024):
        for month in range(1,13):
            ana_data = month_ana[(year,month)]
            value_data = data.get(year,month)
            day_weather = ana_data['白天天气']
            night_weather = ana_data['夜间天气']

            #天气
            weather_name = []
            day_weather_value = []
            night_weather_value = []
            for key in day_weather:
                weather_name.append(key)
            for key in night_weather:
                if key not in weather_name:
                    weather_name.append(key)
            for key in weather_name:
                day_weather_value.append(day_weather.get(key,0))
                night_weather_value.append(night_weather.get(key,0))
            x1 = [i+1 for i in range(len(weather_name))]
            x2 = [i+1.2 for i in range(len(weather_name))]
            plt.figure(figsize=(20,8),dpi=100)
            plt.bar(x1,day_weather_value,width=0.2,label='白天天气',color='r',alpha=0.5)
            plt.bar(x2,night_weather_value,width=0.2,label='夜间天气',color='b',alpha=0.5)
            plt.xlabel('天气')
            plt.ylabel('天数')
            plt.title(f'青岛{str(year)}年{str(month)}月天气情况')
            plt.xticks([i+0.1 for i in x1],weather_name)
            plt.yticks(range(0,30,2))
            plt.grid(linestyle='--',alpha=0.5)
            plt.legend()
            plt.savefig(f'分析结果/月分析/{str(year)}年/{str(year)}年{str(month)}月/图/天气情况.png')
            plt.clf()

            #日温折线图
            x = [i+1 for i in range(len(value_data))]
            x_index = value_data.index
            y1 = value_data['最高气温']
            y2 = value_data['最低气温']
            plt.figure(figsize=(20,8),dpi=100)
            plt.plot(x,y1,label='最高气温',color='r',linestyle='-',linewidth=1,alpha=0.5)
            plt.plot(x,y2,label='最低气温',color='b',linestyle='-',linewidth=1,alpha=0.5)
            plt.xlabel('日期')
            plt.ylabel('温度')
            plt.title(f'青岛{str(year)}年{str(month)}月每日温度')
            plt.xticks(x,x_index,rotation=45)
            plt.yticks(range(-10,40,2))
            plt.grid(linestyle='--',alpha=0.5)
            plt.legend()
            plt.savefig(f'分析结果/月分析/{str(year)}年/{str(year)}年{str(month)}月/图/每日温度.png')
            plt.clf()


def mk_dir():
    try:
        os.mkdir('分析结果')
        os.mkdir('分析结果/年分析')
        os.mkdir('分析结果/月分析')
        for year in range(2020,2024):
            os.mkdir(f'分析结果/年分析/{str(year)}年')
            os.mkdir(f'分析结果/年分析/{str(year)}年/图')
            os.mkdir(f'分析结果/月分析/{str(year)}年')
            for month in range(1,13):
                os.mkdir(f'分析结果/月分析/{str(year)}年/{str(year)}年{str(month)}月')
                os.mkdir(f'分析结果/月分析/{str(year)}年/{str(year)}年{str(month)}月/图')
    except:
        pass