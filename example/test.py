#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib,urllib2  
import socket
import socks
from bs4 import BeautifulSoup
import time
import threading ,time
from time import sleep, ctime
import mysql_handle
import time
import sys

base_url='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'
thread_len=40
li_complete=[0]*thread_len
start_time=time.clock()
count_all=0
result_list=''
count_error=0

def now() :
    return str( time.strftime( '%Y-%m-%d %H:%M:%S' , time.localtime() ) )
#----------模拟浏览器的行为，向谷歌翻译发送数据，然后抓取翻译结果，这就是大概的思路-------
def getChAdmin(url):
    adm1_li=get_Adm1(url)
    adm1_len=len(adm1_li)
    threadpool=[]
    global thread_len
    global li_complete
    for i in range((adm1_len/thread_len)+1):
        start=i*thread_len
        end=(i+1)*thread_len
        if end>=adm1_len: end=thread_len-1
        print("导入组："+str(start)+"--"+str(end))
        th_id=0
        for adm1 in adm1_li[start:end]:
            # time.sleep(5)
            code,name,url=adm1
            # if code not in ['23','41','51','52']:
            #     continue
            printli(adm1)
            insert_item(code,name,'','1')
            adm2_li=get_Adm2(url)
            # print(th_id)
            th = threading.Thread(target= thread_running,args= (adm2_li,th_id))
            threadpool.append(th)
            th_id+=1
        for th in threadpool:
            th.start()
        for th in threadpool:
            th.join()
        print(li_complete)
        li_complete=[0]*thread_len
        print('完成')
        print(count_all,count_error)
        threadpool=[]
        # try:
        #     file_object = open('ch.txt', 'a')
        #     file_object.writelines(result_list)
        #     file_object.close()
        # except:
        #     print('write file error')


def thread_running(adm2_li,th_id):
    print(th_id)
    return
    for adm2 in adm2_li:
        # printli(adm2)
        code,name,url=adm2
        insert_item(code,name,'','2',th_id)
        adm3_li=get_Adm3(url)
        for adm3 in adm3_li:
            # printli(adm3)
            code,name,url=adm3
            insert_item(code,name,'','3',th_id)
            if url =='':continue
            adm4_li=get_Adm4(url)
            for adm4 in adm4_li:
                # printli(adm4)
                code,name,url=adm4
                insert_item(code,name,'','4',th_id)
                adm5_li=get_Adm5(url)
                time.sleep(4)
                for adm5 in adm5_li:
                    # printli(adm5)
                    code,name,vitype=adm5
                    insert_item(code,name,vitype,'5',th_id)

def insert_item(code,name,vitype,level,th_id=None):
    sql="insert into area_update values ('%s','%s','%s','%s')" % (code,name,vitype,level)
    global li_complete
    global count_all
    global count_error
    # global result_list

    # print sql
    try:
        mysql_handle.set_sql('source',sql)
        # unicode(code,'utf-8')
        count_all+=1
        # result_list+=code+u'\t'+(name)+u'\t'+(vitype)+u'\t'+(level)+u'\n'
        if th_id !=None:
            # count_all+=1
            # print (li_complete[th_id])
            li_complete[th_id]+=1
            # print(li_complete)
    except Exception,e:
        count_error+=1
        # print('数据导入出错')
        # print(e)
        if th_id:
            # li_complete[th_id][1]+=1
            pass
    if th_id:
        sys.stdout.flush()
        sys.stdout.write("\rcomplete: %s total: %s error:%s time: %s\r" % (li_complete,count_all,count_error, time.clock()))

def get_soup_html(url):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    #伪装一个IE6.0浏览器访问，如果不伪装，谷歌将返回一个403错误
    browser={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201'}
    # proxy_support = urllib2.ProxyHandler({'http':'http://212.98.137.34:8080'})
    # opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)
    # content = urllib2.urlopen("http://www.baidu.com").read()
    # print(content)
    req = urllib2.Request(url=url,headers=browser)
    #向谷歌翻译发送请求
    count_number=100
    while count_number:
        try:
            # print 1
            response = urllib2.urlopen(req,timeout=3)
            # print 2
            html=response.read()

            soup = BeautifulSoup(html,"html5lib")
            print(html)
            print(soup.prettify())
            # print('-------------------')
            count_number=0
            return soup
        except:
            count_number-=1
    print(url,'download error')
    return BeautifulSoup('',"html5lib")

def get_Adm1(url):
    soup_adm1=get_soup_html(url)
    result=[]
    for tr_item in soup_adm1.find_all(attrs={"class": "provincetr"}):
        for prov in (tr_item.contents):
            # print prov
            link = prov.a['href']
            code=link[0:2]
            name=prov.a.contents[0]
            url_adm2=base_url+link
            # print code,name,url_adm2
            result.append([code,name,url_adm2])
    return result

def get_Adm2(url):
    soup_adm2=get_soup_html(url)
    result=[]
    for tr_item in soup_adm2.find_all(attrs={"class": "citytr"}):
        number=0
        for city in (tr_item.contents):
            link = city.a['href']
            if number%2==0:
                code=city.a.contents[0]
            else:
                name=city.a.contents[0]
                url_adm3=base_url+link
                # print code,name,url_adm3
                result.append([code,name,url_adm3])
            number+=1
    return result

def get_Adm3(url):
    soup_adm3=get_soup_html(url)
    result=[]
    for tr_item in soup_adm3.find_all(attrs={"class": "countytr"}):
        number=0
        for county in (tr_item.contents):
            # print(county)
            if number%2==0:
                try:
                    code=county.a.contents[0]
                except:
                    code=county.contents[0]
            else:
                try:
                    name=county.a.contents[0]
                except:
                    name=county.contents[0]
                try:
                    link = county.a['href']
                    url_adm4=base_url+code[0:2]+'/'+link
                except:
                    url_adm4=''
                result.append([code,name,url_adm4])
                # print code,name,url_adm4
            number+=1
    return result

def get_Adm4(url):
    soup_adm4=get_soup_html(url)
    result=[]
    for tr_item in soup_adm4.find_all(attrs={"class": "towntr"}):
        number=0
        for town in (tr_item.contents):
            # print(county)
            if number%2==0:
                try:
                    code=town.a.contents[0]
                except:
                    code=town.contents[0]
            else:
                try:
                    name=town.a.contents[0]
                except:
                    name=town.contents[0]
                try:
                    link = town.a['href']
                    url_adm5=base_url+code[0:2]+'/'+code[2:4]+'/'+link
                except:
                    url_adm5=''
                result.append([code,name,url_adm5])
                # print code,name,url_adm5
            number+=1
    return result

def get_Adm5(url):
    soup_adm5=get_soup_html(url)
    result=[]
    for tr_item in soup_adm5.find_all(attrs={"class": "villagetr"}):
        number=0
        for village in (tr_item.contents):
            # print(county)
            if number%3==0:
                try:
                    code=village.a.contents[0]
                except:
                    code=village.contents[0]
            elif number%3==1:
                try:
                    vitype=village.a.contents[0]
                except:
                    vitype=village.contents[0]
            else:
                try:
                    name=village.a.contents[0]
                except:
                    try:
                        name=village.contents[0]
                    except:
                        print tr_item.contents
                        # print code,name
                        # print(village)
                        exit()
                result.append([code,name,vitype])
                # print code,name,vitype
            number+=1
    return result

def printli(li):
    temp=''
    for item in li:
        temp=temp+item+' '
    print temp

if __name__ == "__main__":
    # socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    # socket.socket = socks.socksocket
    #Gtext为待翻译的字符串
    getChAdmin(base_url)
    # url=u'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/23/08/230811.html'
    # url2=u'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/51/10/24/511024111.html'
    # url3=u'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/52/27/30/522730102.html'
    # url4=u'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/41/13/03/411303300.html'
    # adm5_li=get_Adm5(url4)
    # # time.sleep(5)
    # for adm5 in adm5_li:
    #     # printli(adm5)
    #     code,name,vitype=adm5
    #     insert_item(code,name,vitype,'5')
    # get_Adm5('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/11/01/08/110108003.html')
    # req = urllib2.Request('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/11/01/08/110108003.html')
    # #伪装一个IE6.0浏览器访问，如果不伪装，谷歌将返回一个403错误
    # browser='Mozilla/4.0 (Windows; U;MSIE 6.0; Windows NT 6.1; SV1; .NET CLR 2.0.50727)'
    # req.add_header('User-Agent',browser)
    # #向谷歌翻译发送请求
    # response = urllib2.urlopen(req)
    # #读取返回页面，然后我们就从这个HTML页面中截取翻译过来的字符串即可
    # html=response.read()
    # print(html)
    # # print(html)
    # soup = BeautifulSoup(html,"html.parser")
    # print(soup)
    # chineseText=Gtranslate(Gtext).strip("'")
    # print('Translated End,The output text: %s' % chineseText)

