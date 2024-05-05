import pymysql
import pandas as pd
from PertreatData import data


class sql():
    def __init__(self,host,user,password,port,db,charset):
        try:
            conn = pymysql.connect(host=host,user=user,password=password,port=port,db=db,charset=charset)
            print('成功连接到数据库')
        except:
            print('连接数据库失败')
        self.conn = conn
        self.coursor = conn.cursor()
        self.data = data


    def add_original_data(self):  #添加原始数据
        print('正在添加已有数据')
        for year in range(2020,2024):
            data = self.data.get_original(year)
            self.add_data(year,data)
        print('已有数据已添加完成')


    def add_data(self,year,data):  #添加数据(data为DataFrame,year为数据年份)
        table_name = str(year) + '年青岛天气数据'
        self.create_table(table_name)
        writer = self.pertreat_data(data)
        self.insert_data(table_name,writer)

    def del_table(self,year):  #删除表
        table_name = str(year) + '年青岛天气数据'
        sql = 'drop table ' + table_name
        try:
            self.coursor.execute(sql)
            self.conn.commit()
            print(f'删除{table_name}表成功')
        except:
            print(f'{table_name}表不存在或删除失败')

    def del_data(self,year,whe):  #删除数据(whe为需要删除的日期,year为数据年份)
        table_name = str(year) + '年青岛天气数据'
        sql = 'delete from ' + table_name + ' where ' + f'date = "{whe}"'
        try:
            self.coursor.execute(sql)
            self.conn.commit()
            print(f'删除{table_name}表中的数据成功')
        except:
            print(f'删除{table_name}表中的数据失败')

    def change_data(self,year,data,whe):  #修改数据(data为list其中不需要包含日期,whe为需要修改的日期,year为数据年份)
        table_name = str(year) + '年青岛天气数据'
        sql = 'update ' + table_name + ' set ' + f'date = "{whe}", weather = "{data[0]}", temperture = "{data[1]}", wind = "{data[2]}"' + ' where ' + f'date = "{whe}"'
        try:
            self.coursor.execute(sql)
            self.conn.commit()
            print(f'修改{table_name}表中的数据成功')
        except:
            print(f'修改{table_name}表中的数据失败')

    def find_data(self,year,weather=0,month=0,day=0,tem=-1):  #查找数据(year为数据年份,weather为天气状况(字符串形式),month为月份,day为日期(形式如'2020-01-01'),tem为温度,0为低于0度,1为高于30度)
        if weather != 0:
            re = self.select_by_weather(year,weather)
            if re == 'error':
                print('查询失败')
                return
            else:
                data = self.select_by_weather(year,weather)
                data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
                data.set_index('日期',inplace=True)
                return data
        if month != 0:
            re = self.select_by_month(year,month)
            if re == 'error':
                print('查询失败')
                return
            else:
                data = self.select_by_month(year,month)
                data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
                data.set_index('日期',inplace=True)
                return data
        if day != 0:
            re = self.select_by_day(year,day)
            if re == 'error':
                print('查询失败')
                return
            else:
                data = self.select_by_day(year,day)
                data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
                data.set_index('日期',inplace=True)
                return data
        if tem == 0:
            re = self.select_underzero(year)
            if re == 'error':
                print('查询失败')
                return
            else:
                data = self.select_underzero(year)
                data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
                data.set_index('日期',inplace=True)
                return data
        if tem == 1:
            re = self.select_high_tem(year)
            if re == 'error':
                print('查询失败')
                return
            else:
                data = self.select_high_tem(year)
                data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
                data.set_index('日期',inplace=True)
                return data
        data = self.select_by_year(year)
        if data == 'error':
            print('查询失败')
            return
        data = pd.DataFrame(data,columns=['日期','天气状况','最低气温/最高气温','风力风向'])
        data.set_index('日期',inplace=True)
        return data

    def close(self):  #关闭数据库
        self.coursor.close()
        self.conn.close()
        print('数据库已关闭')


#以下函数不要调用
    def create_table(self,table_name):  #创建表
        sql = 'create table '+ table_name +'(date char(10), weather varchar(15),temperture varchar(10),wind varchar(20) )'
        try:
            self.coursor.execute(sql)
            self.conn.commit()
            print(f'创建{table_name}表成功')
        except:
            print(f'创建{table_name}表失败或表已存在')

    def insert_data(self,table_name,data):  #插入数据(data为list)
        try:
            print(f'正在向{table_name}表中插入数据')
            for da in data:
                sql = 'insert into ' + table_name + ' values(' + da + ')'
                self.coursor.execute(sql)
                self.conn.commit()
            print(f'向{table_name}表中插入数据成功')
        except:
            print(f'向{table_name}表中插入数据时发生异常')

    def pertreat_data(self,data):  #将数据转化为可写入数据库的形式(data为DataFrame)
        re_data = []
        for index, row in data.iterrows():
            writer = f"'{row['日期']}','{row['天气状况']}','{row['最低气温/最高气温']}','{row['风力风向(夜间/白天)']}'"
            re_data.append(writer)
        return re_data

    def select_by_year(self,year):  #按年查询数据
        table_name = str(year) + '年青岛天气数据'
        sql = 'select * from ' + table_name
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'

    def select_by_month(self,year,month):  #按月查询数据
        if month < 10:
            month = '0' + str(month)
        whe = '____-' + str(month) + '-__'
        table_name = str(year) + '年青岛天气数据'
        sql = 'select * from ' + table_name + ' where date like ' + f'"{whe}"'
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'

    def select_by_day(self,year,day):  #按日查询数据
        table_name = str(year) + '年青岛天气数据'
        sql = 'select * from ' + table_name + ' where date = ' + f'"{day}"'
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'

    def select_by_weather(self,year,weather):  #按天气查询数据
        table_name = str(year) + '年青岛天气数据'
        whe = f'%{weather}%'
        sql = 'select * from ' + table_name + ' where weather like ' + f'"{whe}"'
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'

    def select_underzero(self,year):  #查询低于0度的天气
        table_name = str(year) + '年青岛天气数据'
        sql = 'select * from ' + table_name + ' where temperture like "-%"'
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'

    def select_high_tem(self,year):  #查询高于30度的天气
        table_name = str(year) + '年青岛天气数据'
        sql = 'select * from ' + table_name + ' where temperture like "%/3_℃"'
        try:
            self.coursor.execute(sql)
            data = self.coursor.fetchall()
            return data
        except:
            return 'error'