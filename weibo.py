import requests
import json
import time
import csv


def get_comments(wb_id):
    Data = []
    url = 'https://m.weibo.cn/api/comments/show?id={id}'.format(id=wb_id)
    page_url = 'https://m.weibo.cn/api/comments/show?id={id}&page={page}'
    Resp = requests.get(url, headers=headers, cookies=Cookies)
    page_max_num = Resp.json()['data']['max']
    for i in range(1, page_max_num + 1, 1):
        p_url = page_url.format(id=wb_id, page=i)
        resp = requests.get(p_url, cookies=Cookies, headers=headers)
        resp_data = resp.json()
        data = resp_data['data']['data']  #resp_data.get('data')
        for d in data:
            review_id = d['id']
            like_counts = d['like_counts']
            source = d['source']
            username = d['user']['screen_name']
            image = d['user']['profile_image_url']
            verified = d['user']['verified']
            verified_type = d['user']['verified_type']
            profile_url = d['user']['profile_url']
            comment = d['text']
        time.sleep(1)


def get_Hsin_follower(userId=0):
    url = "https://m.weibo.cn/api/container/getSecond?luicode=10000011&lfid=1005052455640947&uid=2455640947&containerid=1005052455640947_-_FOLLOWERS"
    data = requests.get(url, headers=headers, cookies=Cookies)
    data = data.json()
    maxPage = data['data']['maxPage']

    for page in range(1, maxPage + 1, 1):
        datumList = list()
        pageUrl = "https://m.weibo.cn/api/container/getSecond?luicode=10000011&lfid=1005052455640947&uid=2455640947&containerid=1005052455640947_-_FOLLOWERS&page={page}".format(
            page=page)
        data = requests.get(pageUrl, headers=headers, cookies=Cookies)
        data = data.json()
        for following in data['data']['cards']:
            datum = following['user']['screen_name']
            datumList.append(datum)

        print(datumList)
        writeCSV(datumList)
        time.sleep(0.5)


def writeCSV(datum):
    with open("crawelData.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(datum)


headers = {
    "Host":
    "m.weibo.cn",
    "Referer":
    "https://m.weibo.cn/status/4193146961176576",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
}
Cookies = {
    "Cookie":
    "_T_WM=eebf2816ce83c503f0b74f10c2beb3b7; WEIBOCN_FROM=1110006030; ALF=1517858084; SCF=Aq2M0GCoae-6HpS8XVJ7x9NNT3FeZd9pc5Pogah3lXz35iZmDOpGttl0Biml1XbRf6fccQXt0cn5_SRDlF5UWCc.; SUB=_2A253VVE3DeRhGeRK7lcX9C7FzzuIHXVUtn9_rDV6PUJbktBeLUzxkW1NU1FqRQX-SOvwnWrzgykoJU2biHj3nWE0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF-bOd68M4oqT.4K90Su7EN5JpX5K-hUgL.FozXSK-cSh54ShM2dJLoIpjLxK-L1hzL1h-LxK.L1-zLBKyzMcLVTHLfxr-t; SUHB=0vJJmGs2DMQ2o0; SSOLoginState=1515266407; M_WEIBOCN_PARAMS=luicode%3D20000061%26lfid%3D4193146961176576%26oid%3D4193146961176576%26fid%3D1076035043848646%26uicode%3D10000011"
}
wb_id = 4193146961176576
#get_comments(wb_id)
#get_Hsin_follower()
