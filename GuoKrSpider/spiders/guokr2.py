# -*- coding: utf-8 -*-
import scrapy
from GuoKrSpider.items import GuokrspiderItem
import urllib.parse


class GuokrSpider(scrapy.Spider):
    name = 'guokr2'
    allowed_domains = ['guokr.com']
    start_urls = ['https://www.guokr.com/ask/hottest/?page=1']

    # 'https://www.guokr.com/ask/hottest/?page=1'

    # 浏览页的数据解析
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
            # 此处的item与return有差不多相同的作用，即为会直接返回数据，所以应该在数据完整之后再使用
            # yield item

            # 从详情页的url中获取请求，新建解析方法
            # meta 接受字典{key:item}，在不同的解析函数很直接传递数据
            yield scrapy.Request(item['detail_url'], callback=self.parse_detail, meta={'list_data': item})

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

            # yield scrapy.Request(next_url, callback=self.parse)

            # 3、scrapy提供response.follow
            # 拼接url，构造新的request对象
            yield response.follow(next_url, callback=self.parse)

    # 详情页的数据解析
    def parse_detail(self, response):
        # 使用meta，拿到列表页中的item对象，继续给item添加属性进行赋值
        item = response.meta['list_data']
        div_list = response.xpath('//div[@id="answers"]/div[contains(@class,"answer gclear")]')
        ask_list = list()
        for ask in div_list:
            # item = GuokrspiderItem()
            detail_item = {}
            detail_item['ask_list'] = ask.xpath('.//div[contains(@class,"answerTxt")]/p/text()').extract()
            ask_list.append(detail_item)

        item['detail_list'] = ask_list

        # print(item)
        yield item