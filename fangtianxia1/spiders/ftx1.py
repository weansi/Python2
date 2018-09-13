# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from fangtianxia1.items import Fangtianxia1Item
from urllib import request
import os

class Ftx1Spider(scrapy.Spider):
    name = 'ftx1'
    # allowed_domains = ['xa.fang.anjuke.com']
    # allowed_domains = ['bj.fang.anjuke.com']
    # allowed_domains = ['tj.fang.anjuke.com']
    allowed_domains = ['sh.fang.anjuke.com']
    # start_urls = ['https://xa.fang.anjuke.com/loupan/all/p'+str(x)+'/' for x in range(1,26)]
    # start_urls = ['https://bj.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 16)]
    # start_urls = ['https://tj.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(16, 26)]
    start_urls = ['https://sh.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 3)]
    # def start_requests(self):
    #     urls=[  ['https://xa.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 26)],
    #             ['https://bj.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 26)],
    #             ['https://tj.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 26)],
    #             ['https://sh.fang.anjuke.com/loupan/all/p' + str(x) + '/' for x in range(1, 29)]
    #           ]
    #     for url in urls:
    #          yield scrapy.Request(url=url,callback=self.parse)
             
    def parse(self, response):
        res = response.xpath('//div[@class="key-list"]/div')
        for i in res:
            try:
                item = Fangtianxia1Item()
                item['name'] = i.xpath('div[@class="infos"]/a/h3/span/text()').extract_first()

                item['img_url'] = i.xpath('a/img/@src').extract_first()  # 图片地址
                img_type = item['img_url'].split('.')[-1]
                name1 ='/static/'+ item['name'] + '.' + img_type #拼接的图片保存相对地址
                # print(name1)
                image = r'E:\scrapy_project\fangtianxia1\images/' + name1
                content = request.urlopen(item['img_url']).read()
                with open(image,'wb')as f:
                    f.write(content)
                item['img_urls']=name1

                item['price']=i.xpath('a[@class="favor-pos"]/p').xpath("string(.)").extract_first()
                item['typ'] = i.xpath('div[@class="infos"]/a[4]/div[@class="tag-panel"]/i[2]/text()').extract_first()
                z_url = i.xpath('a/@href').extract_first()
                yield Request(z_url,meta={'key':item},callback=self.parse_content)
            except:
               pass

    def parse_content(self,response):
        item=response.meta['key']
        # item['respon'] = response.xpath('//*[@id="container"]/div[19]/div[1]/div[2]/div/ul').xpath("string(.)").extract_first()
        # print(item['respon'])
        item['addr'] = response.xpath('//div[@id="container"]/div[1]/div[2]/div[1]/dl/dd[4]/span[@class="lpAddr-text"]/text()').extract_first()
        print(item['addr'])

        yield item
