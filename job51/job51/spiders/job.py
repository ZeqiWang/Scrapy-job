# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.http import Request
from job51.items import Job51Item
class JobSpider(scrapy.Spider):

    name = 'job'
    allowed_domains = ['51job.com']
    start_urls = ['http://51job.com/']
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
          # http://search.51job.com/list/000000,000000,0000,00,9,99,python,2,2.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=
    keywords = ['java', 'python', 'c++/c', 'js', '.net', 'R', 'php']

    def parse(self, response):
        for kw in self.keywords:
            one_url = self.url.format(kw,1)
            yield Request(one_url,self.get_page)

    def get_page(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        page_num = soup.find('div', id='resultList').find('div',class_='dw_page').find('div',class_='p_in').find_all('span',class_='td')[0]
        reg = re.compile(r'\d+')
        num = reg.findall(page_num.get_text().encode('utf-8'))[0]
        #获取第一页的href
        for x in range(1,int(num)+1):
            pageone_href =  soup.find('div', id='resultList').find('div', class_='dw_page').find('div',class_='p_in').find( 'ul').find_all('li')[2].find('a')['href']
            index = pageone_href.find('.html')
            l = list(pageone_href)
            l[index-1]=str(x)
            newhref = ''.join(l)
            yield Request(newhref, self.get_hrefs)

    def get_hrefs(self, response):
        hrefs = BeautifulSoup(response.text,'lxml').find_all('div', class_='el')
        for h in hrefs:
            has_tl = h.find('p',class_='t1')
            if has_tl != None:
                href = h.find('p',class_='t1').find('span').find('a')['href']
                yield Request(href,self.parseContent)

    def parseContent(self,response):

        soup = BeautifulSoup(response.text,'lxml')
        content = soup.find('div',class_='tHjob').find('div',class_='cn')
        item = Job51Item()
        item['zwmc'] = content.find('h1')['title'].encode('utf-8')
        item['gzdd'] = content.find('span',class_='lname').get_text().encode('utf-8')
        item['gzxz'] = content.find('strong').get_text().encode('utf-8')
        item['gsmc'] = content.find('p',class_='cname').find('a')['title'].encode('utf-8')
        item['gslx'] = content.find('p',class_='ltype').get_text().encode('utf-8').split('|')[0]

        content1 = soup.find('div',class_='tCompany_main').find('div',class_='jtag').find('div', class_='t1').find_all('span')
        for c in content1:
            if c.find('em', class_='i1') != None:
                item['gzjy'] = c.get_text().encode('utf-8')
                break
            item['gzjy']=''
        for c in content1:
            if c.find('em',class_='i2')!=None:
                item['zdxl'] = c.get_text().encode('utf-8')
                break
            item['zdxl']=''
        for c in content1:
            if c.find('em', class_='i3') != None:
                item['zprs'] = c.get_text()
                break
            item['zprs']=''
        for c in content1:
            if c.find('em', class_='i4') != None:
                fbsj_temp = c.get_text().encode('utf-8')
                item['fbsj'] = fbsj_temp[:fbsj_temp.find('发布')].encode('utf-8')
                break
            item['fbsj'] = ''

        content2 = soup.find('div', class_='tCompany_main').find('p', class_='t2')
        fldy = ''
        if content2 != None:
            spans = content2.find_all('span')
            for c in spans:
                fldy += (c.get_text()+','.encode('utf-8'))
        item['fldy'] = fldy
        return item




