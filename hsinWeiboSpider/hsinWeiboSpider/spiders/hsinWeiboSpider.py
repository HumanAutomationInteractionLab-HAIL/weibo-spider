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

    weiboID = [5676304901]
    start_urls = weiboID
    scrawl_ID = set(start_urls)  # Recording ready ID
    finish_ID = set()  # Recording crwled ID

    def start_requests(self):
        while self.scrawl_ID.__len__():
            ID = self.scrawl_ID.pop()
            self.finish_ID.add(ID)  # Add to crawled ID list
            ID = str(ID)
            global page
            page = 2

            global cookies
            global headersNew
            headersNew = {
                "Host":
                "m.weibo.cn",
                "Connection":
                "keep-alive",
                "User-Agent":
                "Mozilla/5.0 (Linux; Android 6.0.1; LG-F750K Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36"
            }

            cookies = {
                "Cookie":
                "_T_WM=34588bc4ef8dd424b709d5a97b97b4b0; SUB=_2A253ahhlDeRhGeBK6FsY8CrJzT2IHXVUlLgtrDV6PUJbkdBeLWvFkW1NR9H5-0XZ8J3eVn8DgRLdsxch2WRKc7a1; SUHB=0OMkltcq6DUvFB; SCF=AooggcZRunKXIVk9TSOIxNTw-lfAxP1SBtFa-m2nQnnGhF8QYgJlKeAe19dYC2K5NNemqSZ3KTnrdxla7HoY7CQ.; SSOLoginState=1517185077; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode%3D20000174%26lfid%3D1076035580754946%26fid%3D1005051651428902%26uicode%3D10000011"
            }

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
        global numReconnect
        numRreconnect = 10
        try:
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
                informationItems[
                    "Statuses_Count"] = Statuses_Count  #num of weibos
            if Containerid:
                informationItems["Containerid"] = Containerid
                informationItems[
                    "URL"] = "https://m.weibo.cn/%s" % response.meta["ID"]
            yield informationItems
            global firstWeb  #first page of user to be crawled
            firstWeb = response.meta["url_xhr_userinfo"] + "&containerid=" + Containerid

            global pages  #Define total page for a user
            pages = int(Statuses_Count / 10)
            print("total page is ", pages)
        except:
            print("Error occurs and forget about it.")
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
        try:
            if data:
                WeibosItems["Content"] = {}
                WeibosItems["Weibo_Id"] = {}
                WeibosItems["Source"] = {}
                WeibosItems["Attitudes_Count"] = {}
                WeibosItems["Comments_Count"] = {}
                WeibosItems["Created_At"] = {}
                WeibosItems["User"] = {}
                for i in range(10):
                    #if "card_type" in data["data"]["cards"][i]:
                    iStr = str(i)
                    if data["data"]["cards"][i]["card_type"] == 9:
                        Content[i] = data["data"]["cards"][i]["mblog"]["text"]
                        if "retweeted_status" in data["data"]["cards"][i][
                                "mblog"]:
                            Content[
                                i] = "Repost: " + data["data"]["cards"][i]["mblog"]["retweeted_status"]["text"] + " Say:" + Content[i]
                        Weibo_Id[i] = data["data"]["cards"][i]["mblog"]["id"]
                        WeibosItems["Weibo_Id"][iStr] = Weibo_Id[i]
                        #link = re.findall(u"<.*?>", Content[i])
                        #if link:
                        #    for n in range(len(link)):
                        #        Content[i] = re.sub(link[n], "_", Content[i])
                        Content[i] = re.sub("<.*?>", "", Content[i])
                        WeibosItems["Content"][iStr] = Content[i]
                        Source[i] = data['data']["cards"][i]["mblog"]["source"]
                        Attitudes_Count[i] = data['data']["cards"][i]["mblog"][
                            "attitudes_count"]
                        Comments_Count[i] = data['data']["cards"][i]["mblog"][
                            "comments_count"]
                        Created_At[i] = data['data']["cards"][i]["mblog"][
                            "created_at"]
                        User[i] = data['data']["cards"][i]["mblog"]["user"][
                            "screen_name"]
                        #Pics = {}  #pics .data.cards[4].mblog.pics["0"].url
                        #Stream_Url = {}  #media .data.cards["0"].mblog.page_info.media_info.stream_url
                        WeibosItems["Source"][iStr] = Source[i]
                        WeibosItems["Attitudes_Count"][iStr] = Attitudes_Count[
                            i]
                        WeibosItems["Comments_Count"][iStr] = Comments_Count[i]
                        WeibosItems["Created_At"][iStr] = Created_At[i]
                        WeibosItems["User"][iStr] = User[i]
            #informationItems["_id"] = response.meta["ID"]
        except:
            print("Error occurs")
        yield WeibosItems
        page = response.meta["page"] + 1
        if (page <= pages):
            print("current page is ", page)
            next_page = firstWeb + "&page=%s" % page
            try:
                yield scrapy.Request(
                    url=next_page,
                    meta={
                        "page": page,
                    },
                    headers=headersNew,
                    cookies=cookies,
                    callback=self.parseWeibo)  #crawl the next page of weibo
            except:
                time.sleep(1)
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
