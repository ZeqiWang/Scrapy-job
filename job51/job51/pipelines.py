# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

client = pymongo.MongoClient('localhost', 27017)
job = client['test']#创建test数据库   建议python中的名称 和书记库的名称相一致
job51 = job['job51'] #对象名称 和数据库表的名称

class Job51Pipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def process_item(self, item, spider):

        data = {
             'gzxz' : item['gzxz'],  # 职位月薪
             'gzdd' : item['gzdd'],  # 工作地点
             'gslx' : item['gslx'],  # 工作性质
             'gzjy' : item['gzjy'],  # 工作经验
             'zdxl' : item['zdxl'],  # 最低学历
             'zprs' : item['zprs'],  # 招聘人数
             'fbsj' : item['fbsj'],  # 职位类别
             'zwmc' : item['zwmc'],  # 职位名称
             'fldy' : item['fldy'],   # 福利待遇
             'gsmc' : item['gsmc']

        }
        #从数据库中插入数据
        job51.insert_one(data)
        #print (data)

