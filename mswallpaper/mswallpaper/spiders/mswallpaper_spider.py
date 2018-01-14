import scrapy
from mswallpaper.items import MswallpaperItem


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
        images_list = response.xpath('//html/body/main/div[4]/div/div[1]')
        #with open(filename, 'wb') as f:
        #    f.write(moives)
        for image in images_list:
            item["image_urls"] = response.xpath(
                '//div[@class = "grid-item col-sm-6 col-md-4 waves-light waves-effect waves-light infinite-item"]/a/img[@class="z-depth-1"]/@src'
            ).extract()

            yield item
        '''    #re 多页爬虫
            next_page = response.xpath(
                '//span[@class="next"]/a/@href').extract()
        if next_page:
            time.sleep(1)
            url = response.urljoin(next_page[0])
            yield scrapy.Request(url, headers=headers)'''
