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