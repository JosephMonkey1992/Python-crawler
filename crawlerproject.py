"""
crawler-case-lagou
"""
import requests
from bs4 import BeautifulSoup
import time
import json
import pandas as pd


def crawl_detail(id):
    url = 'https://www.lagou.com/jobs/%s.html' % id
    headers = {
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        # 'Cookie':'user_trace_token=20190925025147-35b4249e-b4cd-46a0-bf42-3821cfa8d406; _ga=GA1.2.1267296842.1569351107; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1569351107; LGUID=20190925025148-5cb5a91f-defc-11e9-9561-525400f775ce; JSESSIONID=ABAAABAAAIAACBI5103738CB5E66146CB66DF6CCE598A14; WEBTJ-ID=20190925025200-16d649db5599a5-01755946e665bf-396a4605-921600-16d649db55a966; _gid=GA1.2.832408386.1569351120; index_location_city=%E5%85%A8%E5%9B%BD; X_MIDDLE_TOKEN=555df39e507167750bfef4ab2e54ac4d; TG-TRACK-CODE=index_hotsearch; SEARCH_ID=99e1d19b4ad4487a9394f7d06c17efaf; X_HTTP_TOKEN=a38b62c5f069e2406328839651d04a9da925c4cf18; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1569388236; LGRID=20190925131036-cef44ad9-df52-11e9-a528-5254005c3644',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': None,
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    # time.sleep(2)
    job_bt = soup.find('dd', attrs={'class': 'job_bt'})
    if job_bt is None:
        return
    return job_bt.text


def main():
    url_start = "https://www.lagou.com/jobs/list_%EB0%E6%8D%AE%E5%88%86%E6%9E%90/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/p-city_3?px=default',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    positions = []
    for x in range(1, 31):
        data = {
            'first': 'true',
            'pn': str(x),
            'kd': '数据分析'
        }
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        result = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
        json_result = result.json()
        page_position = json_result["content"]["positionResult"]["result"]
        for position in page_position:
            # 先把需要的信息拿到，不需要的就不要了
            position_dict = {
                'position_name': position['positionName'],
                'work_year': position['workYear'],
                'salary': position['salary'],
                'city': position['city'],
                'district': position['district'],
                'companyShortName': position['companyShortName'],
                'companyLabelList': position['companyLabelList'],
                'companySize': position['companySize'],
                'education': position['education'],
                'financeStage': position['financeStage'],
                'industryField': position['industryField'],
                'skillLables': position['skillLables'],
                'positionAdvantage': position['positionAdvantage'],
                'positionLables': position['positionLables'],
                'company_name': position['companyFullName'],
            }
            position_id = position['positionId']
            # 拿到这个position，然后再去爬这个职位的详情页面
            position_detail = crawl_detail(position_id)
            position_dict['position_detail'] = position_detail
            positions.append(position_dict)
        print('正在爬取第' + str(len(positions) / 15) + '页数据')
        time.sleep(5)
    pf = pd.DataFrame(list(positions))
    columns_list = ['companyShortName', 'city', 'district', 'position_name', 'work_year', 'education',
                    'salary', 'skillLables', 'companySize', 'financeStage', 'companyLabelList',
                    'industryField', 'positionAdvantage', 'positionLables', 'company_name', 'position_detail']
    pf.to_excel('拉勾网爬虫数据.xlsx', index=False, encoding='utf-8', columns=columns_list)
    print("-" * 30)
    print('数据已爬取完毕！')


if __name__ == '__main__':
    main()

"""
my-test
"""
import http.cookiejar
import urllib.request
import requests

requests.packages.urllib3.disable_warnings()

from lxml import etree

from datetime import datetime, timedelta

from threading import Thread

import csv

from math import ceil

import os

import re
from time import sleep
from random import randint

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': str(handler)
}

class WeiboCommentScrapy(Thread):

    def __init__(self,wid):
        global headers
        Thread.__init__(self)
        self.headers = headers
        self.result_headers = [
            '评论者主页',
            '评论者昵称',
            '评论者性别',
            '评论者所在地',
            '评论者微博数',
            '评论者关注数',
            '评论者粉丝数',
            '评论内容',
            '评论获赞数',
            '评论发布时间',
        ]
        if not os.path.exists('comment'):
            os.mkdir('comment')
        self.wid = wid
        self.start()

    def parse_time(self,publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = timedelta(minutes=int(minute))
            publish_time = (datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

    def getPublisherInfo(self,url):
        res = requests.get(url=url,headers=self.headers,verify=False)
        html = etree.HTML(res.text.encode('utf-8'))
        head = html.xpath("//div[@class='ut']/span[1]")[0]
        head = head.xpath('string(.)')[:-3].strip()
        keyIndex = head.index("/")
        nickName = head[0:keyIndex-2]
        sex = head[keyIndex-1:keyIndex]
        location = head[keyIndex+1:]

        footer = html.xpath("//div[@class='tip2']")[0]
        weiboNum = footer.xpath("./span[1]/text()")[0]
        weiboNum = weiboNum[3:-1]
        followingNum = footer.xpath("./a[1]/text()")[0]
        followingNum = followingNum[3:-1]
        followsNum = footer.xpath("./a[2]/text()")[0]
        followsNum = followsNum[3:-1]
        print(nickName,sex,location,weiboNum,followingNum,followsNum)
        return nickName,sex,location,weiboNum,followingNum,followsNum

    def get_one_comment_struct(self,comment):
        # xpath 中下标从 1 开始
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content)==0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content)==0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':')+1:]
        else:
            content = content[0]

        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]

        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]

        publish_time = self.parse_time(publish_time)
        nickName,sex,location,weiboNum,followingNum,followsNum = self.getPublisherInfo(url=userURL)

        return [userURL,nickName,sex,location,weiboNum,followingNum,followsNum,content,praisedNum,publish_time]

    def write_to_csv(self,result,isHeader=False):
        with open('comment/' + self.wid + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if isHeader == True:
                writer.writerows([self.result_headers])
            writer.writerows(result)
        print('已成功将{}条评论写入{}中'.format(len(result),'comment/' + self.wid + '.csv'))

    def run(self):
        res = requests.get('https://weibo.cn/comment/{}'.format(self.wid),headers=self.headers,verify=False)
        commentNum = re.findall("评论\[.*?\]",res.text)[0]
        commentNum = int(commentNum[3:len(commentNum)-1])
        print(commentNum)
        pageNum = ceil(commentNum/10)
        print(pageNum)
        for page in range(pageNum):

            result = []

            res = requests.get('https://weibo.cn/comment/{}?page={}'.format(self.wid,page+1), headers=self.headers,verify=False)

            html = etree.HTML(res.text.encode('utf-8'))

            comments = html.xpath("/html/body/div[starts-with(@id,'C')]")

            print('第{}/{}页'.format(page+1,pageNum))

            for i in range(len(comments)):
                result.append(self.get_one_comment_struct(comments[i]))

            if page==0:
                self.write_to_csv(result,isHeader=True)
            else:
                self.write_to_csv(result,isHeader=False)

            sleep(randint(1,5))

if __name__ =="__main__":
    #声明一个CookieJar对象实例来保存cookie
    cookie = http.cookiejar.CookieJar()
    #HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    WeiboCommentScrapy(wid='IaYZIu0Ko')