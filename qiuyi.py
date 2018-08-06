import requests
from bs4 import BeautifulSoup
import mysql.connector
import re

# -*- coding: utf-8 -*-
# @Author Cong.zhu  #

class qiuyi:

    def __init__(self):
        self.mysql = mysqlhelper()

    # 主方法
    def get_qiuyitype_detail(self,start_url):
        #获取检查类型数据
        list = self.get_main_type_data(start_url)
        #插入检查类型
        self.Insert_main_type(list)
        type_detail_list = [];
        for objlist in list:
            type_detail_html = requests.get(objlist["typeurl"])
            type_detail_html.encoding = 'utf-8'
            type_detail_soup = BeautifulSoup(type_detail_html.text, 'lxml')
            type_detail_name = type_detail_soup.find('div', class_='bd').find('ul', class_='ul_h').findAll(
                target="_blank")
            for type_detail_singer in type_detail_name:
                select_sql = "select type_id from qiuyitype where qiuyitypename='%s'" % objlist["typename"];
                data = self.mysql.select_type_id(select_sql)
                type_detail_list.append(
                    [str(data[0][0]), type_detail_singer.get("title"), type_detail_singer.get("href")])
        #先插入分类明细数据
        self.insert_type_detali(type_detail_list)
        #在去分类明细下面去查找具体的单位，正常值，临床意义
        self.get_type_content(type_detail_list)

    # 获取主页面
    def get_main_html(self,start_url):
        main_html = requests.get(start_url)
        main_html.encoding = 'utf-8'
        main_soup = BeautifulSoup(main_html.text.encode('utf-8'), 'lxml')
        return main_soup

    # 插入主页面检查类型分类
    def Insert_main_type(self,list):
        for objlist in list:
            select_sql = 'select * from qiuyitype where qiuyitypename="%s"' % (objlist["typename"])
            if len(self.mysql.select_type_id(select_sql)) <= 0:
                insert_sql = 'insert into qiuyitype(qiuyitypename,url)  VALUES(%s,%s)'
                data=(objlist["typename"], objlist["typeurl"])
                print(data)
                self.mysql.insert_type_many(insert_sql,data)

    #获取解析主页面检查分类
    def get_main_type_data(self,start_url):
        main_soup = self.get_main_html(start_url);
        qiuyitype = main_soup.find('div', class_='bd').findAll('a', class_='green')
        i = 1
        detail_url = 'http://hyd.qiuyi.cn/jlist/%s.html'
        list = []
        for qiuyisinger in qiuyitype:
            objlist = {
                'id': 0,
                'typename': '',
                'typeurl': ''
            }
            objlist["id"] = i
            objlist["typename"] = qiuyisinger.text
            objlist["typeurl"] = detail_url % i
            list.append(objlist)
            i = i + 1
        return list




    def insert_type_detali(self, type_detail_list):
        insert_sql = "insert into type_detail(`type_id`,`type_detail_name`,`url`) VALUES(%s,%s,%s)"
        for type_detail_obj in type_detail_list:
            select_sql = "select * from type_detail where type_detail_name='%s'" % type_detail_obj[1]
            if len(self.mysql.select_type_id(select_sql)) <= 0:
                data = (type_detail_obj[0], type_detail_obj[1], type_detail_obj[2])
                print(data)
                print(self.mysql.insert_type_many(insert_sql, data))

    #获取解析明细数据
    def get_type_content(self, data):
        for data_one in data:
            type_content = requests.get(data_one[2])
            type_content.encoding = 'utf-8'
            type_content_soup = BeautifulSoup(type_content.text, 'lxml')
            print(data_one[2])
            title_list_soup = type_content_soup.find('div', id='arti_bd222')
            content_list = self.re_content(str(title_list_soup))
            content_list.append(data_one[1])
            print(content_list)
            #获取数据之后插入
            self.insert_content(content_list)

    #插入主体内容数据（单位，正常值，临床意义）
    def insert_content(self, content_list):
        insert_sql = "INSERT into `qiuyi_content`(detail_id,item_id,content) VALUES(%s,%s,%s)"
        select_sql = "select id from type_detail where type_detail_name='%s'" % content_list[3]
        detail_id = self.mysql.select_type_id(select_sql)
        # 单位
        if content_list[0] != "":
            data = (detail_id[0][0], 1, "".join(content_list[0].split()))
            self.mysql.insert_type_many(insert_sql, data)
        # 正常值
        if content_list[1] != "":
            data = (detail_id[0][0], 2, "".join(content_list[1].split()))
            self.mysql.insert_type_many(insert_sql, data)
        # 临床表现
        if content_list[2] != "":
            data = (detail_id[0][0], 3, "".join(content_list[2].split()))
            self.mysql.insert_type_many(insert_sql, data)

    #使用正则去匹配单位，正常值，临床意义
    def re_content(self, data):
        pattern_danwei = re.compile(
            r'class="title">【单位】</div>([\s\S]+?)<br/>'
        )
        pattern_zhengchang = re.compile(
            r'class="title">【正常值】</div>([\s\S]+?)<br/>'
        )
        pattern_lcyy = re.compile(
            r'class="title">【临床意义】</div>([\s\S]+?)<br/>'
        )
        content_list = []
        try:
            content_tuple = pattern_danwei.search(str(data)).group(1)
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', content_tuple)
        except:
            dd = ""
        content_list.append(dd)
        try:
            content_tuple = pattern_zhengchang.search(str(data)).group(1)
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', content_tuple)
        except:
            dd = ""
        content_list.append(dd)
        try:
            content_tuple = pattern_lcyy.search(str(data)).group(1)
            dr = re.compile(r'<[^>]+>', re.S)
            dd = dr.sub('', content_tuple)
        except:
            dd = ""
        content_list.append(dd)
        return content_list


class mysqlhelper:

    #插入数据
    def insert_type_many(self, sql, data):
        conn = mysql.connector.connect(user='root', password='123456', database='qiuyi', use_unicode=True)
        cursor = conn.cursor()
        cursor.execute(sql, data)
        rowcount = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return rowcount

    #查询数据
    def select_type_id(self, sql):
        conn = mysql.connector.connect(user='root', password='123456', database='qiuyi', use_unicode=True)
        cursor = conn.cursor()
        cursor.execute(sql);
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

if __name__ == '__main__':
    qiuyi = qiuyi()
    # 开始的url
    start_url = 'http://hyd.qiuyi.cn/jiancha.html'
    qiuyi.get_qiuyitype_detail(start_url)

