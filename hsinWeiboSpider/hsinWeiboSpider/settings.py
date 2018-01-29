# -*- coding: utf-8 -*-

# Scrapy settings for hsinWeiboSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hsinWeiboSpider'

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "weiboSpider"
MONGODB_COLLECTION = "postsnew"

SPIDER_MODULES = ['hsinWeiboSpider.spiders']
NEWSPIDER_MODULE = 'hsinWeiboSpider.spiders'
#MIDDLEWARES
DOWNLOADER_MIDDLEWARES = {
    "hsinWeiboSpider.middlewares.UserAgentMiddleware": 401,
    "hsinWeiboSpider.middlewares.CookiesMiddleware": 402,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hsinWeiboSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32  #to improve the cpu ability

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 20
CONCURRENT_REQUESTS_PER_IP = 20

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'mswallpaper.middlewares.MswallpaperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'mswallpaper.middlewares.MswallpaperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'mswallpaper.pipelines.MswallpaperPipeline': 300,
#}
#ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
#IMAGES_STORE = 'C:\\Users\\admin\\OneDrive\\git\\weibo-spider\hsinWeiboSpider\\hsinWeiboSpider\\spiders\\hsinWeiboImages'
#IMAGES_EXPIRES = 90
#IMAGES_MIN_HEIGHT = 150
#IMAGES_MIN_WIDTH = 200
## Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 40
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
    'hsinWeiboSpider.pipelines.MongoDBPipeline': 100,
    #'hsinWeiboSpider.pipelines.JsonPipeline': 300,
    #'hsinWeiboSpider.pipelines.CsvPipeline': 200,
}
#FEED_FORMAT = "csv"
#FEED_URI = "C:\\Users\\admin\\OneDrive\\git\\weibo-spider\\hsinWeiboSpider\\hsinWeiboSpider\\spiders\\collected.csv"