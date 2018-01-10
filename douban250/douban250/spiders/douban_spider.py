# -*- coding: utf-8 -*-
import scrapy
import time
from douban250.items import Douban250Item


class douban250(
        scrapy.Spider
):  #scrapy.spider is base class, all spider should be inherited from it

    name = "douban250"

    def start_requests(self):
        allowed_domains = [
            "movie.douban.com"
        ]  #allowed_domains 可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
        start_urls = ["https://movie.douban.com/top250"]
        global headers
        headers = {
            "Referer":
            "https://movie.douban.com/",
            "Host":
            "movie.douban.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        }
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        item = Douban250Item()
        filename = "douban250file"
        moives = response.xpath('//ol[@class="grid_view"]/li')
        #with open(filename, 'wb') as f:
        #    f.write(moives)
        for moive in moives:
            item["ranking"] = moive.xpath(".//em/text()").extract(
            )  #Xpath从当前路径.开始/xpath应该尽量精准例如额外[@calss=“11”]
            item["movie_name"] = moive.xpath(
                './/span[@class="title"][1]/text()').extract()  # 1 xpath中指代第一个
            item["score"] = moive.xpath(
                ".//span[@class='rating_num']/text()").extract()
            item["commenter_nums"] = moive.xpath(
                './/div[@class="star"]//span[last()]/text()').re(u'(\d+)人评价')[
                    0]  #0 指代第一个list中指代第一个
            yield item
            #re 多页爬虫
            next_page = response.xpath(
                '//span[@class="next"]/a/@href').extract()
        if next_page:
            time.sleep(1)
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, headers=headers)
