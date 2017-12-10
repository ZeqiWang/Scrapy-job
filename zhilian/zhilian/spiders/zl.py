# -*- coding: utf-8 -*-

import scrapy  # 导入scrapy包

from bs4 import BeautifulSoup
from scrapy.http import Request  ##一个单独的request的模块，需要跟进URL的时候，需要用它
from zhilian.items import ZhilianItem

class ZlSpider(scrapy.Spider):
    name = 'zl'
    #allowed_domains = ['sou.zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/']
    baseUrl = "http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3b160400%3b160000%3b160500%3b300100&jl=%E9%80%89%E6%8B%A9%E5%9C%B0%E5%8C%BA&kw={}&isadv=0&sg=eb2df7b4fd7b401aae61118c55ed72ec&p={}"
    keywords = ['java', 'python', 'c++/c', 'js', '.net', 'R', 'php']

    def parse(self, response):
        for kw in self.keywords:
            max_page = 90
            for x in range(1, max_page+1):
                url = self.baseUrl.format(kw, x)

                yield Request(url, self.get_job_href)

    def get_job_href(self, response):
        node_list = BeautifulSoup(response.text, 'lxml').find('div',id='newlist_list_content_table').find_all("table")
        for node in node_list:
            if node.find('td',class_='zwmc')!= None:
                href = node.find('td',class_='zwmc').find_all('a')[0]['href']
                #self.f.write(href + "\n")
                yield Request(href, self.get_info)

    def get_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.find('ul',class_='terminal-ul').find_all('li')
        item = ZhilianItem()
        item['zwyx'] = infos[0].find("strong").get_text().encode('utf-8')#职位月薪
        item['gzdd'] = infos[1].find("strong").find('a').get_text().encode('utf-8')  # 工作地点
        item['gzxz'] = infos[3].find("strong").get_text().encode('utf-8')#工作性质
        item['gzjy'] = infos[4].find("strong").get_text().encode('utf-8')#工作经验
        item['zdxl'] = infos[5].find("strong").get_text().encode('utf-8')#最低学历
        item['zprs'] = infos[6].find("strong").get_text().encode('utf-8')  # 招聘人数
        item['zwlb'] = infos[7].find("strong").find('a').get_text().encode('utf-8')  # 职位类别
        item['zwmc'] = soup.find('div',class_='top-fixed-box').find('h1').get_text().encode('utf-8') #职位名称
        #fldy_list = soup.find('div', class_='welfare-tab-box').find_all('span')

        #print (item)
        return item

