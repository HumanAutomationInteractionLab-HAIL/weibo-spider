# encoding=utf-8
import re
import datetime
#from scrapy.spider import CrawlSpider
#from scrapy.selector import Selector
#from scrapy.http import Request
from hsinWeiboSpider.items import InformationItem, WeibosItem, FollowsItem, FansItem
import scrapy
import json
import time
from hsinWeiboSpider.weiboId import weiboID


class Spider(scrapy.Spider):
    name = "hsinWeiboSpider"
    host = "https://m.weibo.cn"
    #id = 1993586607
    #for n in range(500):
    #    id = id + 3
    #    weiboId = weiboId.append(id)
    weiboId=[5676304901]
    start_urls = weiboID
    scrawl_ID = set(start_urls)  # Recording ready ID
    finish_ID = set()  # Recording crwled ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)  # Add to crawled ID list
            ID = str(ID)

            global headersNew
            headersNew = {
                "Host":
                "m.weibo.cn",
                "Connection":
                "keep-alive",
                "User-Agent":
                "Mozilla/5.0 (Linux; Android 6.0.1; LG-F750K Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
            }
            global cookies
            cookies = {
                "Cookie":
                "_T_WM=82575ffe7f3daaf9abd2f2d385385225; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031724367710%26fid%3D1005055580754946%26uicode%3D10000011"
                #" _T_WM=bb0f26cfaec31b1b64566a1e21e88e0b; SUHB=0A0IP5POp5orr_; SCF=ApAI1z-zWWPUna8W3sAgo508dFgkXxfdhwvX0uRRYtbKNMPKelKHr1dzona_D9BKV6OCRJydN_uDZei5GoiwaQ0.; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=fid%3D1076035580754946%26uicode%3D10000011"
            }
            global page
            page = 300
            url_mainSite = "https://m.weibo.cn/%s" % ID
            url_xhr_userinfo = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s" % ID

            yield scrapy.Request(
                url=url_xhr_userinfo,
                meta={
                    "ID": ID,
                    "url_xhr_userinfo": url_xhr_userinfo,
                    "headersNew": headersNew,
                    "cookies": cookies,
                },
                headers=headersNew,
                cookies=cookies,
                callback=self.parseMProfile)  # Crawl profile from User id

    def parseMProfile(self, response):

        informationItems = InformationItem()
        data = json.loads(response.body)
        if data:
            NickName = data["data"]["userInfo"]["screen_name"]
            Statuses_Count = data["data"]["userInfo"][
                "statuses_count"]  #Number of weibos
            Gender = data["data"]["userInfo"]["gender"]
            Num_Follows = data["data"]["userInfo"]["follow_count"]
            Num_Fans = data["data"]["userInfo"]["followers_count"]
            Containerid = data["data"]["tabsInfo"]["tabs"][1][
                "containerid"]  #Container ID

        informationItems["_id"] = response.meta["ID"]
        if NickName:
            informationItems["NickName"] = NickName
        if Gender:
            informationItems["Gender"] = Gender
        if Num_Follows:
            informationItems["Num_Follows"] = Num_Follows
        if Num_Fans:
            informationItems["Num_Fans"] = Num_Fans
        if Statuses_Count:
            informationItems["Statuses_Count"] = Statuses_Count  #num of weibos
        if Containerid:
            informationItems["Containerid"] = Containerid
            informationItems["URL"] = "https://m.weibo.cn/%s" % response.meta[
                "ID"]
        yield informationItems
        global firstWeb  #first page of user to be crawled
        firstWeb = response.meta["url_xhr_userinfo"] + "&containerid=" + Containerid

        global pages  #Define total page for a user
        pages = int(Statuses_Count / 10)
        print("total page is ", pages)
        yield scrapy.Request(
            url=firstWeb,
            meta={
                "Containerid": Containerid,
                "firstWeb": firstWeb,
                "pages": pages,
                "page": page
            },
            headers=headersNew,
            cookies=cookies,
            callback=self.parseWeibo)  # Go crawling weibo

    def parseWeibo(self, response):

        WeibosItems = WeibosItem()
        data = json.loads(response.body)

        Content = {}
        Weibo_Id = {}
        Source = {}  # iphone6 .data.cards[9].mblog.source
        Attitudes_Count = {}  #.data.cards["0"].mblog.attitudes_count
        Comments_Count = {}  #.data.cards["0"].mblog.comments_count
        Created_At = {}  #.data.cards["0"].mblog.created_at
        User = {}  #.data.cards["0"].mblog.user.screen_name
        #Pics = {}  #pics .data.cards[4].mblog.pics["0"].url
        #Stream_Url = {}  #media .data.cards["0"].mblog.page_info.media_info.stream_url
        if data:
            WeibosItems["Content"] = {}
            WeibosItems["Weibo_Id"] = {}
            WeibosItems["Source"] = {}
            WeibosItems["Attitudes_Count"] = {}
            WeibosItems["Comments_Count"] = {}
            WeibosItems["Created_At"] = {}
            WeibosItems["User"] = {}
            for i in range(10):
                if "card_type" in data["data"]["cards"][i]:
                    if data["data"]["cards"][i]["card_type"] == 9:
                        Content[i] = data["data"]["cards"][i]["mblog"]["text"]
                        if "retweeted_status" in data["data"]["cards"][i]["mblog"]:
                            Content[
                                i] = "Repost: " + data["data"]["cards"][i]["mblog"]["retweeted_status"]["text"] + " Say:" + Content[i]
                        Weibo_Id[i] = data["data"]["cards"][i]["mblog"]["id"]
                        WeibosItems["Weibo_Id"][i] = Weibo_Id[i]
                        link = re.findall(u"<.*?>", Content[i])
                        if link:
                            for n in range(len(link)):
                                Content[i] = re.sub(link[n], "_", Content[i])
                        WeibosItems["Content"][i] = Content[i]
                        Source[i] = data['data']["cards"][i]["mblog"]["source"]
                        Attitudes_Count[i] = data['data']["cards"][i]["mblog"][
                            "attitudes_count"]
                        Comments_Count[i] = data['data']["cards"][i]["mblog"][
                            "comments_count"]
                        Created_At[i] = data['data']["cards"][i]["mblog"]["created_at"]
                        User[i] = data['data']["cards"][i]["mblog"]["user"][
                            "screen_name"]
                        #Pics = {}  #pics .data.cards[4].mblog.pics["0"].url
                        #Stream_Url = {}  #media .data.cards["0"].mblog.page_info.media_info.stream_url
                        WeibosItems["Source"] = Source[i]
                        WeibosItems["Attitudes_Count"] = Attitudes_Count[i]
                        WeibosItems["Comments_Count"] = Comments_Count[i]
                        WeibosItems["Created_At"] = Created_At[i]
                        WeibosItems["User"] = User[i]
        #informationItems["_id"] = response.meta["ID"]
        yield WeibosItems

        page = response.meta["page"] + 1
        max_page = 100
        if (page <= pages) and (page <= max_page):
            print("current page is ", page)
            next_page = firstWeb + "&page=%s" % page
            yield scrapy.Request(
                url=next_page,
                meta={
                    "page": page,
                },
                headers=headersNew,
                cookies=cookies,
                callback=self.parseWeibo)  #crawl the next page of weibo

    def parseMoreProfile(self, response):
        informationItems = InformationItem()
        data = json.loads(response.body)
        if data:
            Location = data["data"].cards["0"].card_group[4].item_content
            Statuses_Count = data["data"]["userInfo"]["statuses_count"]
