# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# define the scrapy.Fields for your item here like:
# name = scrapy.scrapy.Field()
class InformationItem(scrapy.Item):  #Personal profile
    _id = scrapy.Field()
    NickName = scrapy.Field()  # 昵称
    Gender = scrapy.Field()  # 性别
    #Province = scrapy.Field()  # 所在省
    #City = scrapy.Field()  # 所在城市
    #Signature = scrapy.Field()  # 个性签名
    #Birthday = scrapy.Field()  # 生日
    Statuses_Count = scrapy.Field()  # 微博数
    Num_Follows = scrapy.Field()  # 关注数
    Num_Fans = scrapy.Field()  # 粉丝数
    #Sex_Orientation = scrapy.Field()  # 性取向
    #Marriage = scrapy.Field()  # 婚姻状况
    URL = scrapy.Field()  # 首页链接
    Containerid = scrapy.Field()  #Containerid


class WeibosItem(scrapy.Item):  #微博信息 """
    Weibo_Id = scrapy.Field()  # ID
    User = scrapy.Field()  # 用户
    # Content = scrapy.Field()  # 微博内容
    Created_At = scrapy.Field()  # 发表时间
    Co_oridinates = scrapy.Field()  # 定位坐标
    Source = scrapy.Field()  # 发表工具/平台
    Attitudes_Count = scrapy.Field()  # 点赞数
    Comments_Count = scrapy.Field()  # 评论数
    Transfer = scrapy.Field()  # 转载数
    Content = scrapy.Field()


class FollowsItem(scrapy.Item):  #关注人列表 """
    _id = scrapy.Field()  # 用户ID
    follows = scrapy.Field()  # 关注


class FansItem(scrapy.Item):  # 粉丝列表 """
    _id = scrapy.Field()  # 用户ID
    fans = scrapy.Field()  # 粉丝
