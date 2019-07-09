# -*- coding: utf-8 -*-

"""
--------------------------------------------------------
# @Version : python3.7
# @Author  : wangTongGen
# @File    : spider.py
# @Software: PyCharm
# @Time    : 2019/7/8 08:54
--------------------------------------------------------
# @Description: this code is programed to crawl the
                information of credit among the people
--------------------------------------------------------
"""

import re
import os
import sys
import time
import json
import requests


class CreditPersonSpider(object):

    def __init__(self, pageNum, savePath):
        self.pageNum = pageNum
        self.hasNext = True
        self.savePath = savePath
        self.kw = requests.utils.quote("失信被执行人查询")
        self.url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query="+self.kw+"&pn={}&rn=10&ie=utf-8&oe=utf-8&format=json"
        self.headers = {
                        "Host": "sp0.baidu.com",
                        "Connection": "keep-alive",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
                        "Accept": "*/*",
                        "Referer": "https://www.baidu.com/s?tn=50000023_hao_pg&ie=utf-8&sc=UWd1pgw-pA7EnHc1FMfqnHRvnWRknHR3nHDkPiuW5y99U1Dznzu9m1Y1P1RLnHf4nH6Y&ssl_sample=normal&srcqid=3271362467293291044&f=3&rsp=4&H123Tmp=nunew7&word={}".format(requests.utils.quote("失信被执行人查询")),
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.8"
                        }

    def parse_url(self, url):
        response = None
        try:
            response = requests.get(url, timeout=(3, 7), headers=self.headers).content.decode()
        except Exception as e:
            print("-"*100)
            num = int(re.findall('&pn=(.*?)&rn', url)[0])
            print("Exception happened...."+"_"*10+str(num//10+1))
            self.write2log(num)

        finally:
            return response

    def write2log(self, num):
        with open("log.txt", "a", encoding='utf-8') as f:
            f.write(num+"\n")

    def get_credict_person_info(self, str_list):
        if str_list:
            item = {}
            for line in str_list:
                item["iname"] = line['iname'] if line['iname'] else None
                item['cardNum'] = line['cardNum'] if line['cardNum'] else None
                item['publishDate'] = line['publishDate'] if line['publishDate'] else None
                # print(line['iname'], line['cardNum'], line['publishDate'])

                yield item

    def write2csv(self, items):
        # if not os.path.exists(self.savePath):
        #     os.mkdir(self.savePath)

        with open(self.savePath, "a", encoding="utf-8") as f:
            # f.write("iname,cardNum,publishDate\n")
            for item in items:
                # print(item['iname'] + ',' + item['cardNum'] + ',' + item['publishDate'])
                # f.write(json.dumps(item, ensure_ascii=False))
                # f.write("\n")
                f.write(item['iname']+','+item['cardNum']+','+item['publishDate']+'\n')

    def spider_running(self):
        # self.pageNum = 1
        while self.hasNext:
            pageNum = (self.pageNum-1)*10
            print("开始爬取第{}页".format(self.pageNum))
            url = self.url.format(pageNum)
            print(url)
            response = self.parse_url(url)

            if response is not None:
                json_str = json.loads(response)
                has_info = json_str.get("data")
                if has_info:
                    self.hasNext = (has_info[0]['MoreResult']=="1")
                    # 获取信息
                    items = self.get_credict_person_info(has_info[0]['result'])
                    self.write2csv(items)
                    # 爬取下一页


            self.pageNum += 1
            time.sleep(5)

    def test(self):

        url = self.url.format(930)
        print("开始爬取")
        print(url)
        response = self.parse_url(url)
        json_str = json.loads(response)
        has_next = json_str['data'][0]['MoreResult']
        print(has_next)
        self.hasNext = True if has_next else False
        print(self.hasNext)
        # 获取信息
        items = self.get_credit_person_info(json_str.get("data")[0]['result'])
        self.write2csv(items)

    def run(self):
        print("spider running........")

        # self.test()
        self.spider_running()
        print("spider stopped...")


if __name__ == '__main__':

    ##  For running on Linux

    # if len(sys.argv) != 2:
    #     print("input error!")
    #     print("you should input like this: python spider.py --pageNum=1")
    # elif sys.argv[1].split("=")[0] != "--pageNum":
    #     print("you should input the parameter --pageNum")
    # else:
    #     key, pageNum = sys.argv[1].split("=")
    #     spider = CreditPersonSpider(pageNum)
    #     spider.run()

    # For Pycharm

    pageNum = 8194 # 增量式爬虫，选择从第几页开始爬取
    savePath = "data_7920.csv"
    spider = CreditPersonSpider(pageNum, savePath)
    spider.run()
