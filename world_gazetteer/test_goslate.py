#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib,urllib2  
import socket
import socks
from bs4 import BeautifulSoup
import random
#----------模拟浏览器的行为，向谷歌翻译发送数据，然后抓取翻译结果，这就是大概的思路-------
html = ''
def Gtranslate(text):  
    if isinstance(text,unicode):
        text = text.encode('utf-8')
    # proxy_list = [
    #     '122.248.240.177:3128',
    #     '119.81.130.2:3128',
    #     '128.199.99.190:8888',
    #     '128.199.103.49:8080',
    #     '128.199.232.117:3128',
    #     '128.199.208.154:3128',
    #     # '128.199.210.98:443',
    #     '119.81.111.230:8080',
    #     '180.210.200.129:3128',
    #     '202.167.248.186:80',
    #     '118.189.69.34:3128',
    #     '119.81.232.136:8080'
    # ]
    # proxy  = random.choice(proxy_list)
    # urlhandle  = urllib2.ProxyHandler({'http':proxy})
    # opener  = urllib2.build_opener(urlhandle)
    # urllib2.install_opener(opener)

    #text 输入要翻译的英文句子  


    #hl:浏览器、操作系统语言，默认是zh-CN
    #ie:默认是UTF-8
    #text：就是要翻译的字符串
    #langpair:语言对，即'en'|'zh-CN'表示从英语到简体中文
    values={}
    values['client']='t'
    values['sl']='auto'
    values['tl']='zh-CN'
    values['hl']='en'

    # values['dt']='bd' 设置返回对翻译出词语的名词及其它词性解释
    values['dt']='bd'

    # values['dt']='t' 设置返回翻译时给定的唯一的最佳解释
    # values['dt']='t'

    # values['dt']='ex'
    # values['dt']='rw'
    # values['dt']='qca'
    # values['dt']='rm'
    # values['dt']='md'
    # values['dt']='ld'
    values['ie']='UTF-8'
    values['oe']='UTF-8'
    values['rom']=1
    values['otf']=1
    values['ssel']=0
    values['tsel']=0
    values['pc'] = 1
    values['srcrom'] = 0
    values['kc']=1
    values['tk']= getChar()
    values['source']='bh'
    values['q']=text
    #URL用来存储谷歌翻译的网址

    #将values中的数据通过urllib.urlencode转义为URL专用的格式然后赋给data存储
    data = urllib.urlencode(values)
    url='http://translate.google.cn/translate_a/single'
    # 添加dt=t 即返回唯一的最佳解释
    url = url + "?"+data +'&dt=t'
    # print url
    #然后用URL和data生成一个request
    req = urllib2.Request(url)
    #伪装一个IE6.0浏览器访问，如果不伪装，谷歌将返回一个403错误
    header={}
    browser='Mozilla/4.0 (Windows; U;MSIE 6.0; Windows NT 6.1; SV1; .NET CLR 2.0.50727)'
    header['User-Agent']=browser
    header['Accept']='*/*'
    header['Cache-Control']='max-age=0'
    header['Accept-Encoding']='gzip, deflate, sdch'
    header['Accept-Language']='zh-CN,zh;q=0.8,en;q=0.6'
    header['Connection']='keep-alive'
    header['Host']='translate.google.cn'
    header['Referer']='http://translate.google.cn/?hl=en'
    header['X-Client-Data']='CKK2yQEIqbbJAQjBtskBCP2VygE='
    req.headers=header
    # req.add_header(header)
    # print(req.__class__)

    # print(req.encode('utf-8'))
    global html
    html = ''
    #向谷歌翻译发送请求

    #读取返回页面，然后我们就从这个HTML页面中截取翻译过来的字符串即可
    count_number=5
    while count_number:
        try:
            response = urllib2.urlopen(req,timeout=5)
            global html
            html=response.read()
            count_number=0
        except:
            count_number-=1
    if not isinstance(html,unicode):
        html = html.decode('utf-8')
    # print html
    result = getResult(html)

    return result[0]

def getChar():
    a = ''
    b = ''
    for i in range(6):
        if i==0:
            a +=str(random.randint(1,9))
        else:
            a += str(random.randint(0,9))
        b += str(random.randint(0,9))
    return  a+'.'+b

def getResult(html):
    index = html.find("noun")
    # 存在名词的时候
    if(index>=0):
        start = html.find('[',index)
        end = html.find(']',index)
    else:
        start = html.find("\"",0)
        end = html.find("\"",start+1)
    ans = html[start+1:end]
    ans = ans.replace("\"","")
    result = ans.split(',')
    return result

if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket

    #Gtext为待翻译的字符串 
    # Gtext='you should believe yourself,you are the best one! and we sure that you will do something making us being proud of you'
    # Gtext="to"
    # print('The input text: %s' % Gtext)
    Words = [
        'Aba Island',
        'HaiNan',
        'Setting',
        'University',
        'Shanghai',
        'TaiWan Island',
        'province',
    ]
    for i in range(100):
        text = random.choice(Words)
        ans = Gtranslate(text)
        print ans
    # print('Translated End,The output text: %s' % chineseText)
