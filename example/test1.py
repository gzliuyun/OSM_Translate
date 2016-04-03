#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib,urllib2  
import socket
import socks
from bs4 import BeautifulSoup

#----------模拟浏览器的行为，向谷歌翻译发送数据，然后抓取翻译结果，这就是大概的思路-------
def Gtranslate(text):  

    #text 输入要翻译的英文句子  
    Gtext=text

    #hl:浏览器、操作系统语言，默认是zh-CN
    #ie:默认是UTF-8
    #text：就是要翻译的字符串
    #langpair:语言对，即'en'|'zh-CN'表示从英语到简体中文




    values={'hl':'zh-CN','ie':'UTF-8','text':Gtext,'langpair':"'zh-CN'|'en'"}
    values={}
    values['client']='t'
    values['sl']='auto'
    values['tl']='zh-CN'
    values['hl']='en'
    values['dt']='bd'
    # values['dt']='ex'
    # values['dt']='t'
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
    values['kc']=1
    values['tk']=898935.758670
    values['source']='bh'
    values['q']='setting'
    #URL用来存储谷歌翻译的网址

    #将values中的数据通过urllib.urlencode转义为URL专用的格式然后赋给data存储
    data = urllib.urlencode(values)
    url='http://translate.google.cn/translate_a/single'
    url = url + "?"+data
    print(url)
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
    print(req.__class__)

    # print(req.encode('utf-8'))

    #向谷歌翻译发送请求  
    response = urllib2.urlopen(req)
    #读取返回页面，然后我们就从这个HTML页面中截取翻译过来的字符串即可
    html=response.read()
    print(html)
    a=BeautifulSoup(html,'lxml',from_encoding='gzip')
    print(a.prettify())
    #使用正则表达式匹配<=TRANSLATED_TEXT=)。而翻译后的文本是'TRANSLATED_TEXT='等号后面的内容
    p=re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
    m=p.search(html)
    print(m.group())
    chineseText=m.group(0).strip(';')
    return chineseText
  
if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
    socket.socket = socks.socksocket
    #Gtext为待翻译的字符串 
    # Gtext='you should believe yourself,you are the best one! and we sure that you will do something making us being proud of you'
    # Gtext="to"
    # print('The input text: %s' % Gtext)
    Gtranslate('')
    # print('Translated End,The output text: %s' % chineseText)