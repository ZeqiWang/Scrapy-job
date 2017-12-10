# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo

client = pymongo.MongoClient('localhost', 27017)
test = client['test']#创建test数据库   建议python中的名称 和书记库的名称相一致
zhilian = test['zhilian'] #对象名称 和数据库表的名称
class ZhilianPipeline(object):

    # def __init__(self):
    #     self.f = open("zhilian.json","w")
    #
    # def process_item(self, item, spider):
    #     content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
    #     self.f.write(content)
    #     return item

    def process_item(self, item, spider):

        data = {
             'zwyx' : item['zwyx'],  # 职位月薪
             'gzdd' : item['gzdd'],  # 工作地点
             'gzxz' : item['gzxz'],  # 工作性质
             'gzjy' : item['gzjy'],  # 工作经验
             'zdxl' : item['zdxl'],  # 最低学历
             'zprs' : item['zprs'],  # 招聘人数
             'zwlb' : item['zwlb'],  # 职位类别
             'zwmc' : item['zwmc'],  # 职位名称
             #'fldy' : item['fldy']   # 福利待遇
        }
        #从数据库中插入数据
        zhilian.insert_one(data)
        #print (data)
        for item1 in zhilian.find():


            print (item1)
