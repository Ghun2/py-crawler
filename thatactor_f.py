# parser.py
import requests
from bs4 import BeautifulSoup as bs
import sys
import os
import datetime

from pymongo import MongoClient

new = []

def scrape_html(url):
    req = requests.get(url)
    return bs(req.text, 'html.parser')


def mongoConnection(dict):
    client = MongoClient('localhost', 27017)
    db = client.test
    col = db.ActorRecruit

    col.insert_one(dict)

    # result = col.find({})

def check_time():
    utcnow = datetime.datetime.utcnow()
    time_gap = datetime.timedelta(hours=9)
    now = utcnow + time_gap
    nowday = now.strftime('%Y-%m-%d')
    nowtime = now.strftime('%H:%M:%S')
    return [str(nowday),str(nowtime)]

def logging(txt):
    f = open("log.txt",'a')   #로그 file open
    curr_time = check_time()
    f.write(curr_time[0] + ' ' + curr_time[1] + ' ' + txt + '\n')
    f.close()

def latest_Data_ex():
    res = []
    with open('latest.txt', 'r+') as f_read:
        for _ in range(10):
            before = f_read.readline()
            before = before.rstrip('\n')
            res.append(before)
        f_read.close()
        return res

def latest_Data_in(newlat):
    with open('latest.txt', 'w+') as f_write:
        for val in newlat :
            f_write.write(str(val)+'\n')
        f_write.close()

# for v in result:
#     print(v)

# sys.exit()
# init_count = 3
# for i in range(init_count,0,-1):
def parse_flim_web(page,lat):
    global new

    soup = scrape_html('https://www.filmmakers.co.kr/index.php?mid=actorsAudition&page='+str(page))
    my_titles = soup.select(
        '#board > tbody > tr > td.title > a'
        )

    # print(my_titles)

    my_titles.pop(0)
    my_titles.pop(0)

    # my_titles는 list 객체
    for oneTitle in my_titles:
        dicTemp = {
            'title':'',
            'making':'',
            'name':'',
            'director':'',
            'part':'',
            'preproduction':'',
            'castingStar':'',
            'period':'',
            'pay':'',
            'numRecruit':'',
            'sexRecruit':'',
            'chargeMan':'',
            'tel':'',
            'mail':'',
            'closingDate':'',
            'article':'',
            'srl':'',
            'type':'',
            'date':'',
            'time':'',
            'img':''
        }
        # Tag안의 텍스트
        # print(oneTitle.text)
        # # Tag의 속성을 가져오기(ex: href속성)
        # print(oneTitle.get('href'))
        # print(oneTitle.get('href').split('document_srl=')[1])

        ch_srl = oneTitle.get('href').split('document_srl=')[1]



        for val in lat:
            if str(ch_srl) == val :
                return 0

        soup2 = scrape_html(oneTitle.get('href'))
        # soup2 = scrape_html('https://www.filmmakers.co.kr/actorsAudition/4340780')


        #####
        tmp = soup2.find('div',{'id':'board'})#.find('div',{'class':'col-md-8 col-lg-8 padding-0'})#.find('div',{'class':'container-fluid padding-0'})
        # .find('div',{'class':'padding-0 margin-top-5 margin-bottom-0'}).find('tbody').find('tr'))
        tmp = tmp.find_all('div')
        tmp = tmp[1].find('div',{'class':'container-fluid padding-0'})

        if tmp.find('form') != None :
            continue

        itime = tmp.find('table').find_all('td')[7].find('span').text

        itime = itime.replace('년 ','-').replace('월 ','-').replace('일 ',' ').replace('시 ',':').replace('분 ',':').replace('초','').split()
        # print(itime)



        # print(str(nowday),str(nowtime))
        # sys.exit()


        tmp = tmp.find_all('div')

        # print(tmp)

        art = tmp[1].find_all('p')

        arTemp = ''
        for value in art:
            arTemp += value.text + '\n'

        imgart = tmp[1].find_all('img')
        # print(imgart)

        if len(imgart) != 0:
            imTemp = '{'

            for index in range(len(imgart)) :
                if len(imgart)-1 == index :
                    imTemp += str(imgart[index].get('src')) + '}'
                else :
                    imTemp += str(imgart[index].get('src')) + ','

            dicTemp['img'] = imTemp

        tbl = tmp[0].find_all('td')

        # print(tbl)
        # for value in tbl:
            # print(value.text)
        # print()

        # sys.exit()
        # print(oneTitle.find('strong').text.strip().replace('[','').replace(']',''))
        # print(oneTitle.find('span').text)
        dicTemp['srl'] = ch_srl
        try:
            dicTemp['type'] = oneTitle.find('strong').text.strip().replace('[','').replace(']','')
        except :
            dicTemp['type'] = ''
        dicTemp['title'] = oneTitle.find('span').text.strip()
        dicTemp['making'] = tbl[0].text
        dicTemp['name'] = tbl[1].text
        dicTemp['director'] = tbl[2].text
        dicTemp['part'] = tbl[3].text
        dicTemp['preproduction'] = tbl[4].text
        dicTemp['castingStar'] = tbl[5].text
        dicTemp['period'] = tbl[6].text
        dicTemp['pay'] = tbl[7].text
        dicTemp['numRecruit'] = tbl[8].text
        dicTemp['sexRecruit'] = tbl[9].text
        dicTemp['chargeMan'] = tbl[10].text
        dicTemp['tel'] = tbl[11].text
        dicTemp['mail'] = tbl[12].text
        dicTemp['closingDate'] = tbl[13].text
        dicTemp['article'] = arTemp
        dicTemp['date'] = itime[0]
        dicTemp['time'] = itime[1]

        # print(dicTemp)
        # sys.exit()
        mongoConnection(dicTemp)

        if len(new) < 10 :
            new.append(dicTemp['srl'])
        # print(ch_srl,new)

        # logging('index = '+str(page)+' inner srl = '+dicTemp['srl'])
    print('index = ',page)
    return 1
