# -*- coding: utf-8 -*-
import scrapy
from GuoKrSpider.items import GuokrspiderItem


class GuokrSpider(scrapy.Spider):
    name = 'guokr'
    allowed_domains = ['guokr.com']
    start_urls = ['https://www.guokr.com/ask/hottest/?page=1']
    # 'https://www.guokr.com/ask/hottest/?page=1'

    def parse(self, response):
        # 取到数据的标签
        # li_list = response.xpath('/html/body/div[3]/div[1]/ul[2]/li')
        li_list = response.xpath('//ul[@class="ask-list-cp"]/li')
        # '/html/body/div[3]/div[1]/ul[2]'
        # print('*' * 100)
        # print(li_list)
        # print('*' * 100)
        # print(response.xpath('/html/body/div[3]/div[1]/ul[2]/li[2]/div[2]/h2/a/text()').extract_first())

        # 遍历取出数据
        for li in li_list:
            item = GuokrspiderItem()
            # item = {}
            # 标题和url
            # '/html/body/div[3]/div[1]/ul[2]/li[1]/div[2]/h2/a'
            # 标题中的表情是无法正常显示的，如果在此报错是正常
            item['title'] = li.xpath('.//a/text()').extract_first().strip()
            item['detail_url'] = li.xpath('.//h2/a/@href').extract_first().strip()

            # 描述
            # '/html/body/div[3]/div[1]/ul[2]/li[1]/div[2]/p'
            item['desc'] = li.xpath('./div[2]/p/text()').extract_first().strip()

            # 关注数 '/html/body/div[3]/div[1]/ul[2]/li[1]/div[1]/p[1]/span'
            item['focus_num'] = li.xpath('.//div[1]/p[1]/span/text()').extract_first().strip()

            # 回答数
            # '/html/body/div[3]/div[1]/ul[2]/li[1]/div[1]/p[2]/span'
            item['ask_num'] = li.xpath('.//div[1]/p[2]/span/text()').extract_first().strip()

            # 标签
            # '/html/body/div[3]/div[1]/ul[2]/li[1]/div[2]/div/p/a'
            item['tags'] = li.xpath('.//div[2]/div/p/a/text()').extract()

            # print(item)
            yield item


