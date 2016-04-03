#__author__ = 'Administrator'
# -*- coding: utf-8 -*-

import mysql_handle
import google_translate
import time
import re
import thread_select
import test_goslate
UFI = []
COUNT = 0
NUMTEST = 0
ufi_name ={}
def find_UFI():
    database = 'source'
    countries = 'countries'
    places = 'places'

    # sql = """create table nat_en_ch as select distinct UFI as id from %s""" % (countries)
    # print(sql)
    # mysql_handle.set_sql(database,sql)

    sql = """ select distinct UFI from %s where UFI>-10 and UFI<=-1""" % (countries)
    global UFI
    a = mysql_handle.get_select(database,sql)
    UFI = get_result_list(a)
    print len(UFI)


def get_list(index):
    database='source'
    nat_en_ch = 'nat_en_ch'
    countries = 'countries'
    places = 'places'

    a = index*(-10)
    b = (index-1)*(-10)
    sql = """select %s.UFI, %s.NT, %s.FULL_NAME_ND_RO, %s.FULL_NAME_ND_RG, %s.FULL_NAME_RO, %s.FULL_NAME_RG,%s.SORT_NAME_RO,
             %s.SORT_NAME_RG from %s where %s.UFI>%s and %s.UFI<=%s """ % (countries,countries,countries,countries,countries,countries,countries,countries,countries,countries,str(a),countries,str(b))
    print (sql)
    a = mysql_handle.get_select(database,sql)
    ufi_dect = get_ufi_dict(a)

    for i,j in ufi_dect.items():
        v= ufi_dect.get(i)
        print i,
        for l in range(len(v)):
            # c = v[l].encode('utf-8')
            c = v[l]
            print c,'|',
        print

    get_result_list(database,ufi_dect)
def insert_to_table(ufi):
    global ufi_name
    database = 'source'
    table = 'nat_en_ch'
    ufi_dict = {}
    na = ''
    en = ''
    ch = ''
    ufi_dict = ufi_name.get(ufi)
    for k,v in ufi_dict.items():
        if k == 'na':
            na = v
        elif k=='en':
            en = v
        elif k=='ch':
            ch = v
    sql = """insert into %s(UFI,native_name,english_name,chinese_name) values(%s,'%s','%s','%s') """ % (table,ufi,na,en,ch)
    mysql_handle.set_sql(database,sql)

def get_ufi_dict(res):
    # UFI 所对应的所有变名集合
    ufi_dict = {}
    # UFI所对应的地名（本地语言 及 英文）
    global  ufi_name
    for i in range(len(res)):
        ufi = res[i][0]
        if not ufi_dict.has_key(ufi):
            ufi_dict[ufi] = []
        language = res[i][1]
        for j in range(2,len(res[i])):
            temp=res[i][j]
            if len(temp) == 0:
                continue
            if isinstance(temp,unicode) == False:
                temp=str(temp)
            if temp not in ufi_dict[ufi]:
                ufi_dict[ufi].append(temp)

            if not ufi_name.has_key(ufi):
                ufi_name[ufi] = {}
            if language=='NS':
                if not ufi_name[ufi].has_key('na'):
                    ufi_name[ufi]['na'] = temp
            else:
                if not ufi_name[ufi].has_key('en'):
                    ufi_name[ufi]['en'] = temp

    return ufi_dict

# 打印sql结果
def print_sql_res(res):
    for i in range(len(res)) :
        output=''
        for j in range(len(res[i])):
            temp=res[i][j]
            # print(temp)
            if isinstance(temp,unicode)==False:
                temp=str(temp)
            temp_len=len(temp.encode('gb2312'))
            output=output+temp+(20-temp_len)*' '+''
            # print(output)
        print(output)
    print("查询结果长度："+str(len(res)))

def get_result_list(database,ufi_list):
    places = 'places'
    global UFI

    length = len(ufi_list)
    global  NUMTEST
    NUMTEST += length

    for i in ufi_list:
        transified = 0
        print 'UFI= ',i
        for k in range(len(ufi_list[i])):
            name = ufi_list[i][k]
            if isinstance(name,unicode):
                name = name.encode('utf-8')
            sql = """select %s.ch_name from %s where %s.rom_name = "%s" """ %(places,places,places,name)
            print(sql)
            a = mysql_handle.get_select(database,sql)
            if len(a)==0:
                continue
            # 返回的a是查询到的中文地名
            print (u'查询: ',a[0][0])
            global ufi_name
            ufi_name[i]['ch'] = a[0][0]
            transified = 1
            break
        if transified==0:
            for k in range(len(ufi_list[i])):
                Gtext = ufi_list[i][k]
                print (Gtext)
                # chineseText = google_translate.Gtranslate(Gtext).strip("'")
                chineseText = test_goslate.Gtranslate(Gtext)
                print chineseText

                if len(chineseText)>0 and is_chinese(chineseText):
                    chineseText = strip_tag(chineseText)
                    print(u'谷歌: '+chineseText)

                    global ufi_name
                    ufi_name[i]['ch'] = chineseText
                    transified = 1
                    break
        if transified==1:
            global COUNT
            COUNT+= 1
        # insert_to_table(i)
        print "____________________________________________________"

# //自实现strip('`‘“')函数
def strip_tag(str):
    copy_str = ''
    tag = [u'`',u'‘',u'“']
    if not isinstance(str,unicode):
        str = unicode(str,"utf-8")
    for i in range(len(str)):
        if str[i] in tag:
            continue
        else:
            copy_str +=  str[i]
    str = copy_str
    return str

 # 判断字符串是否全是汉字
def is_chinese(str):
    str = strip_tag(str)
    if not isinstance(str,unicode):
        str = unicode(str,"utf-8")
    for k in range(len(str)):
        uchar = str[k]
        if (uchar <= u'\u4e00' or uchar >=u'\u9fa5') and uchar != u'\xb7' :
            return False
    return True

if __name__ == "__main__":
    start = time.time()
    # find_UFI()
    get_list()
    # print is_chinese("中国")

    end = time.time()
    print 'time: ',end-start

