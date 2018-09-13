# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings
from scrapy.exceptions import DropItem#抛出异常
from scrapy import log


from scrapy import Request
#要使用scrapy的imagespipeline，必须安装pillow模块
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

dbuser='root'
dbname='ai6'
dbpass='123456'
dbhost='127.0.0.1'
dbport='3306'
class Fangtianxia1Pipeline(object):
    def __init__(self):
        self.conn=pymysql.connect(user=dbuser,passwd=dbpass,db=dbname,host=dbhost,charset='utf8')
        self.cursor=self.conn.cursor()#创建游标
        # self.cursor.execute('truncate anjuke')  # 清空数据库表
        # self.cursor.execute('truncate anjuke_bj')#清空数据库表
        # self.cursor.execute('truncate anjuke_tj')  # 清空数据库表
        # self.cursor.execute('truncate anjuke_sh')  # 清空数据库表
        # self.cursor.execute('truncate type')#清空数据库表
        # self.conn.commit()

    def process_item(self, item, spider):
        # 使用游标执行数据插入数据库
        self.cursor.execute("insert into anjuke_sh(name,img_urls,typ,price,addr)values(%s,%s,%s,%s,%s)",(item['name'],item['img_urls'],item['typ'],item['price'],item['addr']))
        # self.cursor.execute("insert into anjuke_sh(respon)values(%s)",(item['respon']))
        # pid=self.conn.insert_id()
        # self.cursor.execute("insert into type(t_name,pid,jzmj)values(%s,%s,%s,%s)",(item['name'],pid,item['jzmj']))
        self.conn.commit()
        return item



