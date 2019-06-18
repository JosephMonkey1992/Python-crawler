# Python Crawler
## Top Interview
- [2.Checking IP Address](#2checking-IP-address)  
- [3.mimic user agent and proxy IP address](#3.mimic-user_agent-and-proxy-IP-address)  
- [4.get all IPO companies from 2010 to 2018 via NASDAQ](#4.get-all-IPO-companies-from-2010-to-2018-via-NASDAQ)  
- [5.spliting](#5.spliting)  
- [6.fetch data from S-1 form SEC](#6.fetch-data-from-S-1-form-SEC) 
- [7.fetch P/E ratio from yahoo and NASDAQ](#7.fetch-P/E-ratio-from-yahoo-and-NASDAQ) 
- [8.get current stock price](#8.get-current-stock-price) 
### 2.Checking IP Address
get host name and check IP address
```python
import socket
socket.gethostname() 
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
print(get_host_ip())
```
### 3.mimic user_agent and proxy IP address
import necessary packages->find proxy IP Address->add user agent->try decode the street.com
```python
import urllib
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from urllib.request import urlopen
import re
import time
import datetime
import csv
import sys
import codecs
import string
import random
import socket
import http.cookiejar
##The IP agent which is obtained from agent website. Besides, we can purchase from T-Mall.
proxy_list={
    'http':'157.230.220.233:8080',   
    'http':'45.55.46.222:8080',  
    'https':'204.48.18.225:8080',
    'http':'198.211.109.90:8080',
    'https':'159.203.184.52:3128',
    'http':'157.230.210.133:8080',
    'http':'198.211.103.89:80',
    'http':'134.209.125.125:8080',
    'http':'157.230.232.130:8080',
    'http':'206.189.231.239:8080',
    'http':'104.248.7.88:3128'
            }           
##example of how we use headers, to mimic human searching avoid being detected as machine.
url100='https://www.thestreet.com/quote/SCTY.html'
req100=urllib.request.Request(url100)
req100.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
html100=urllib.request.urlopen(req100,timeout=500).read()
html100 = bytes.decode(html100,encoding="utf-8")
print(html100)
##without the headers we cannot get into TheStreet website. However,for Sec and Nasdaq dont worry about that.
```
### 4.get all IPO companies from 2010 to 2018 via NASDAQ
create a year-month list->get href->fetch target informaton->print->restore in csv
```python
##creating an url list, which can help us to open hundreds of web pages to search for IPO companies from 2010 to 2018. 
y=['2010','2011','2012','2013','2014','2015','2016','2017','2018']
m=['01','02','03','04','05','06','07','08','09','10','11','12']
##url_list=prior url +year+month.
url_list=['https://www.nasdaq.com/markets/ipos/activity.aspx?tab=pricings&month='+a+'-'+b for a in y for b in m]
for item in url_list:
    print(item)
target_list=list()
for item0 in url_list:
    html0=urllib.request.urlopen(item0).read()
    soup0 = BeautifulSoup(html0)
    soup0.prettify()    
    for anchor in soup0.find_all('a', href=True): ##find the link to open new page from the previous one.
        a=anchor['href']
        if('https://www.nasdaq.com/markets/ipos/company/' in a):
            target=a
            target_list.append(target)
##create necessary information list we need, otherwise the loop only rememebr the last call.
symbol_list=list()
name_list=list()
address_list=list()
phone_list=list()
employees_list=list()
issueprice_list=list()
shareoutstanding_list=list()
CIK_list=list()
years_list=list()
for item1 in target_list:
    response1=urllib.request.urlopen(item1)
    soup1=BeautifulSoup(response1, 'html.parser')
    for title1 in soup1.find_all('title'):
        title1_txt=title1.get_text()
        symbol=re.findall(r'[(](.*?)[)]', title1_txt) ##pulling out the value here between "()" to get symbol.
        for table1 in soup1.find_all('table'):
                table1_txt=table1.get_text()
                if('Company Name' in table1_txt):
                        td1=table1.find_all('td')
                        for i in range(len(td1)):
                            tdtext1=td1[i].get_text()
                            if('Company Name' in tdtext1):
                                name=td1[i+1].get_text()
                                address=td1[i+3].get_text()
                                phone=td1[i+5].get_text()
                                employees=td1[i+11].get_text()
                                issueprice=td1[i+23].get_text()
                                shareoutstanding=td1[i+35].get_text()
                                CIK=td1[i+43].get_text()
                                years=td1[i+17].get_text()
                                name_list.append(name)
                                address_list.append(address)
                                phone_list.append(phone)
                                employees_list.append(employees)
                                issueprice_list.append(issueprice)
                                shareoutstanding_list.append(shareoutstanding)
                                CIK_list.append(CIK)
                                years_list.append(years)
                                symbol_list.append(symbol)
##see the results and check correctness.
print(name_list)
print(address_list)
print(phone_list)
print(employees_list)
print(issueprice_list)
print(shareoutstanding_list)
print(CIK_list)
print(years_list)
print(symbol_list)
##write a csv.file to record the results.
with open('information-final.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(name_list)
    f_csv.writerow(address_list)
    f_csv.writerow(phone_list)
    f_csv.writerow(employees_list)
    f_csv.writerow(issueprice_list)
    f_csv.writerow(shareoutstanding_list)
    f_csv.writerow(CIK_list)
    f_csv.writerow(years_list)
    f_csv.writerow(symbol_list)
```
### 5.spliting 
create two lists->split and refine
```python
symbol_list=list()
for item2 in url_list:
    req = urllib.request.urlopen(item2).read()
    soup2 = BeautifulSoup(req)
    soup2.prettify()    
    for anchor2 in soup2.find_all('a', href=True):
        a=anchor2['href']
        if('https://www.nasdaq.com/symbol/' in a):
            smb=a
            symbol_list.append(smb)           
Technology_list=list()
for s in symbol_list:
    page2 = urllib.request.urlopen(s).read()
    soup3 = BeautifulSoup(page2)
    soup3.prettify()
    for an in soup3.find_all('a', href=True):
        h=an['href']
        if('https://www.nasdaq.com/screening/companies-by-industry.aspx?industry=Technology'in h):
            select1=s
            Technology_list.append(select1)           
##check the tech list.
print(Technology_list)
Healthcare_list=list()
for v in symbol_list:
    page3 = urllib.request.urlopen(v).read()
    soup4 = BeautifulSoup(page3)
    soup4.prettify()
    for anc in soup4.find_all('a', href=True):
        g=anc['href']
        if('https://www.nasdaq.com/screening/companies-by-industry.aspx?industry=Health%2bCare'in g):
            select2=v
            Healthcare_list.append(select2)            
##check the health list
print(Healthcare_list)
##spliting the necessary word:
fin1_list=list()
for t in range(len(Technology_list)):
    res1=Technology_list[t].split('/') ##get the symbol
    fin1=res1[len(res1)-1]    
    fin1_list.append(fin1) 
print(fin1_list)
fin2_list=list()
for j in range(len(Healthcare_list)):
    res2=Healthcare_list[j].split('/')
    fin2=res2[len(res2)-1]
    fin2_list.append(fin2)  
print(fin2_list)
##store into csv
with open('Technology.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(fin1_list)
    f_csv.writerow(Technology_list)   
with open('Healthcare.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(fin2_list)
    f_csv.writerow(Healthcare_list)
```  
### 6.fetch data from S-1 form SEC
important to prunedd and use dictionary
```python
url_list=list()
with open('CIKlist.csv', newline='', encoding='UTF-8') as csvfile:
    reader=csv.reader(csvfile)
    for p in reader:
        u=str(p) ##we need to make those into string
        prunedd=u.strip(string.punctuation) ##sttrip all the unnecessary pounctuation.like ''.
        url='https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=000'+prunedd+'&type=S-1&dateb=&owner=exclude&count=40'
        url_list.append(url)      
print(url_list)
page_list=list()
for item in url_list:
    response5=urllib.request.urlopen(item)
    soup = BeautifulSoup(response5,features="lxml")
    td=soup.find_all('td')       
    for i in range(len(td)):
        tdtxt=td[i].get_text()
        if('S-1'==tdtxt):
            tdn=td[i+1]
            for ah in tdn.find_all('a'):
                page=ah['href']
                page_list.append(page)              
print(page_list)
url_list2=list()
for m in page_list:
    pa='https://www.sec.gov'+m
    url_list2.append(pa)    
print(url_list2)
page1_list=list()
for h in url_list2:
    response6=urllib.request.urlopen(h)
    soup1 = BeautifulSoup(response6,features="lxml")
    td1=soup1.find_all('td')       
    for g in range(len(td1)):
        tdtxt1=td1[g].get_text()
        if('1'==tdtxt1):
            tdn1=td1[g+2]
            for ah1 in tdn1.find_all('a'):
                page1=ah1['href']
                page1_list.append(page1)              
print(page1_list)
url_list3=list()
for n in page1_list:
    paa='https://www.sec.gov'+n
    url_list3.append(paa)    
print(url_list3)
with open('urlsecondlevel.csv','w') as wow: ##We need to store the temporate results, because the next step the machine is gonna visit thousands of time.Not necessary if you have 4 hours seating infront of computer.
    wow_csv = csv.writer(wow)
    wow_csv.writerow(url_list3)
##The urlsecondlevel.csv carries the same data with Level.csv.
##Create dictionary
dic={}
with open('Level.csv', newline='', encoding='UTF-8') as woww:
    readerw=csv.DictReader(woww)
    for row in readerw:
        dic[row['\ufeffCIK']]=row['URLF']
##applying for dict to match each CIK and URL, because it contains dupicated url previously.
for k,v in dic.items(): 
    print(k)
    print(v) 
stockoption_list=list()
CIKlist=list()
for k,v in dic.items():
    response7=urllib.request.urlopen(v)
    soup7 = BeautifulSoup(response7,features="lxml")
    td7=soup7.find_all('td')       
    for l in range(len(td7)):
        tdtxt7=td7[l].get_text()
        if('weighted average exercise price' in tdtxt7):##by searching weighted average excerse price we can have the stock option, incentive plan information with outstanding or granted prices.
            try:
                tdn7=td7[l].get_text()
            except IndexError:
                pass
            stockoption_list.append(tdn7)
            CIKlist.append(k)
with open('NEWstockoption.csv', 'w', encoding='utf-8') as file:
    stock=csv.writer(file)
    stock.writerow(stockoption_list)
    stock.writerow(CIKlist)
```
### 7.fetch P/E ratio from yahoo and NASDAQ
when dealing with bundle of data, try to store the temporary results.
```python
dic={}
with open('selected.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dic[row['ï»¿Name']]=row['symbolurl']
        print(row)     
PEr_list=list()
CIKlist=list()
for k,v in dic.items(): 
    with urlopen(v) as text:
        soup = BeautifulSoup(text, 'html.parser')
        for table in soup.find_all('table'):
            table_txt=table.get_text()
            if('Forward P/E (1y)' in table_txt): ##fetching Forward PE ration from Nasdaq.
                td=table.find_all('td')
                for i in range(len(td)):
                    td_txt=td[i].get_text()
                    if('Forward P/E (1y)' in td_txt):
                        spanr=td[i].get_text()
                        PEr_list.append(spanr)
                        CIKlist.append(k)                      
print(PEr_list)
with open('PEPPratio.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(PEr_list)
    f_csv.writerow(CIKlist)   
PEE_list=list()
CIK_list=list()
for k,v in dic.items(): 
    with urlopen(v) as text:
        soup = BeautifulSoup(text, 'html.parser')
        for table in soup.find_all('table'):
            table_txt=table.get_text()
            if('P/E Ratio' in table_txt): ##fetching real PE ration from Nasdaq.
                td=table.find_all('td')
                for i in range(len(td)):
                    td_txt=td[i].get_text()
                    if('P/E Ratio' in td_txt):
                        span=td[i].get_text()
                        PEE_list.append(span)
                        CIK_list.append(k)                      
print(PEE_list)
with open('PEEratio.csv','w') as ff:
    ff_csv = csv.writer(ff)
    ff_csv.writerow(PEE_list)
    ff_csv.writerow(CIK_list)   
##some of the results from Nasdaq shows that some companies they have NE for both PE and Forward PE, so we decide to search the missing ones from Yahoo.
dic={}
with open('notincluded.csv', newline='', encoding='UTF-8') as toy: ##not included in Previous results but still be our targets.
    readertoy=csv.DictReader(toy)
    for row in readertoy:
        dic[row['\ufeffSymbol']]=row['CIK']     
k_list=list()
for k,v in dic.items():
    url3='https://finance.yahoo.com/quote/'+k+'?p='+k+'&.tsrc=fin-srch'
    k_list.append(url3) 
print(k_list)
CIK_list2=list()
EPSlist2=list()
name_list=list()
for k,v in dic.items():
    url3='https://finance.yahoo.com/quote/'+k+'?p='+k+'&.tsrc=fin-srch'
    with urlopen(url3) as text2:
        soup2 = BeautifulSoup(text2, 'html.parser')
        td1=soup2.find_all('td')
        for x in range(len(td1)):
            tdtxt=td1[x].get_text()
            if('EPS (TTM)' in tdtxt):
                eps=td1[x+1].get_text()
                CIK_list2.append(v)
                name_list.append(k)
                EPSlist2.append(eps)              
with open('yahooeps.csv','w') as yahoo:
    yahoo_csv = csv.writer(yahoo)
    yahoo_csv.writerow(name_list)
    yahoo_csv.writerow(CIK_list2)
    yahoo_csv.writerow(EPSlist2)
```
### 8.get current stock price
this version without timer
```python
def get_price(url1):
    with urlopen(url1) as text:
        soup = BeautifulSoup(text, 'html.parser')
        for p in soup.find_all('p'):
            p_txt=p.get_text()
            if('The current last sale of' in p_txt):
                spantxt=p.find_all('span')
                for i in range(len(spantxt)):
                    data=spantxt[i].get_text()
                    if('The current last sale of' in data):
                        try:
                            price=spantxt[i+1].get_text()
                            if("$" in price):
                                pruned_txt=price.strip(string.punctuation)
                                return pruned_txt # get rid of () $ punctuations
                        except IndexError:
                             pass                          
dic={}
with open('Currentprice-Selectedgroup.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dic[row['symbolname']]=row['symbolurl']      
price_list=list()
CIK_list=list()
Time_list=list()
for k,v in dic.items():
    url1="https://www.nasdaq.com/symbol/"+k
    p=get_price(url1)
    T=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ##get local time
    if(p is not None):
            rep=p.split('$')
            rep2=rep[len(rep)-1]
            rep3=float(rep2)
            price_list.append(rep3)
    CIK_list.append(k)
    Time_list.append(T)
    print("CIK:", k)
    print("Localtime:", T)
    print("Current Price:", rep3)  
##store into csv by column
with open('currentprice20190602.csv','w') as f:
    f_csv = csv.writer(f)
    for i in range(len(price_list)):
        f_csv.writerow([CIK_list[i], Time_list[i], price_list[i]])
```
