import scrapy
from mswallpaper.items import MswallpaperItem
import re
import time


class mswallpaper(scrapy.Spider):
    name = "mswallpaper"

    def start_requests(self):
        
        allowed_domains = [
            "wallpaperstudio10.com"
        ]  #allowed_domains 可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
        start_urls = [
            "https://wallpaperstudio10.com/wallpaper-category-quotes.html",
        ]
        global headers
        headers = {
            "Referer":
            "https://wallpaperstudio10.com/",
            "Host":
            "wallpaperstudio10.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        }
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        item = MswallpaperItem()
        #filename = "douban250file"
        images_list = response.xpath('//div[@class="tz-gallery"]')
        #with open(filename, 'wb') as f:
        #    f.write(moives)
        for image in images_list:
            strUrl = response.xpath(
                '//div[@class = "grid-item col-sm-6 col-md-4 waves-light waves-effect waves-light infinite-item"]/a/img[@class="z-depth-1"]/@src'
            ).extract()
            i = 0
            for url in strUrl:
                newUrlGroup = re.match(u'(.*?)560x315(.*)', url)
                imageUrl = newUrlGroup.group(
                    1) + "1920x1080" + newUrlGroup.group(2)
                strUrl[i] = imageUrl
                i += 1
            print("bigurl", strUrl)
            item["image_urls"] = strUrl
            yield item
            #re 多页爬虫
            next_page = response.xpath(
                '//div[@class="text-center col-md-12 m-top-20 m-bot-20"]//a/i[@class="fa fa-caret-right"]//parent::a/@href'
            )
            print("next_page", next_page)
            next_page = next_page.re(u".*?(\?page.*)")
            print("next_page", next_page)
            break
        if next_page:
            url = response.urljoin(next_page[0])
            print("url", url)
            yield scrapy.Request(url, headers=headers)
