# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zwyx = scrapy.Field()  # 职位月薪
    gzdd = scrapy.Field()  # 工作地点
    gzxz = scrapy.Field()  # 工作性质
    gzjy = scrapy.Field()  # 工作经验
    zdxl = scrapy.Field()  # 最低学历
    zprs = scrapy.Field()  # 招聘人数
    zwlb = scrapy.Field()  # 职位类别
    zwmc = scrapy.Field()  # 职位名称
    #fldy = scrapy.Field()  #福利待遇