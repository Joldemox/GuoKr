# -*- coding: utf-8 -*-
import scrapy
from GuoKrSpider.items import GuokrspiderItem
import urllib.parse


class GuokrSpider(scrapy.Spider):
    name = 'guokr1'
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

        # 翻页
        # 假设翻页没有规律，找下一页标签，然后构造新的request对象发送请求
        # '/html/body/div[3]/div[1]/ul[3]/li[6]/a'
        # 也可以根据文本定位标签'//a @[text()='下一页']/@href'
        next_url = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_url is not None:
            '''在scrapy中构造新的请求对象'''
            # 使用yield生成器进行返回给引擎
            # callback注明使用具体的回调函数

            '''需要补充完整的url地址'''
            # 1、直接拼接：next_url = 'https://www.guokr.com' + next_url
            # next_url = 'https://www.guokr.com' + next_url

            # 2、导入urllib.parse，自动拼接url
            # url.parse.urljoin(完整的url, 不完整的url)
            # next_url = urllib.parse.urljoin(response.url, next_url)

            # 3、scrapy提供response.follow
            yield response.follow(next_url, callback=self.parse)

            # yield scrapy.Request(next_url, callback=self.parse)
