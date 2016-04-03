#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'usr'

import sys
import mysql_handle
import mysql_crud_example
import google_coordinate as locate

database='source'
table1 = 'area_change'
table2 = 'ch_administrative_a'
table3 = 'provinces'

city_black_list=[u'市辖区',u'县',u'河南省直辖县级行政区划',u'湖北省直辖县级行政区划',u'海南省直辖县级行政区划',u'新疆自治区直辖县级行政区划']
county_black_list=[u'市辖区']

#对省份（level = 1）进行匹配
def set_province():
    sql1 = '''SELECT code,a.level,a.name FROM %s a WHERE a.level = 1 ''' %(table1)
    result_area = mysql_handle.get_select(database,sql1)      #二重元组((,,),(,,),...)
    print len(result_area)

    count_res_0 = 0
    count_res_1 = 0
    count_res_2 = 0

    for i in range(len(result_area)):
        #逐条取result_area中的记录，并赋值
        item = result_area[i]                #(u'110100000000', 2L, u'\u5e02\u8f96\u533a')
        code = item[0]                       #area_change表中地级市代码：130100000000
        level = item[1]                      #area_change表中地级市级别：2
        name = item[2]                       #area_change表中地级市名称：石家庄市

        #取出省份code在area_change表中对应的省份名称
        sql_get_prov_name = '''select name from %s where code = "%s" ''' %(table1,prov)
        prov_name = mysql_handle.get_select(database,sql_get_prov_name)[0][0]
        all_name = prov_name + name

        #取出code在provinces表中对应的adm1
        sql_get_prov_code = '''select adm1 from %s where code = "%s" ''' %(table3,prov)
        adm1 = mysql_handle.get_select(database,sql_get_prov_code)[0][0]               #get_select  ((u'22',),)

        #省份相同，级别相同，名称相同，从'ch_administrative_a'表提取相应信息
        sql2 = '''select ufi,lat,lon,cc1,lc from %s
                  WHERE adm1 = "%s" and substr(dsg,4,1) = "%s" and full_name_nd_ro = "%s" ''' %(table2,adm1,level,name)
        admin_res=mysql_handle.get_select(database,sql2)   #((-1903688L, u'39.932273', u'116.41002', u'CH', u'zho'),)
        admin_len=len(admin_res)            #判断是否有重复条数

        if admin_len == 0:
            print admin_res
            lat,lon = locate.get_coordinates(all_name)
            ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            print(ufi,lat,lon,country,lc,000000)
            count_res_0 += 1

        elif admin_len == 1:
            ufi,lat,lon,country,lc=admin_res[0]
            print(ufi,lat,lon,country,lc,111111)
            count_res_1+=1

        else:
            lat,lon = locate.get_coordinates(all_name)              #google经纬度
            tmp_list = []                                           #与google经纬度差值
            for i in range(admin_len):
                item = admin_res[0]
                tmp_lat,tmp_lon = item[1],item[2]
                tmp_list.append(abs(lat - float(tmp_lat)) + abs(lon - float(tmp_lon)))
            min_of_list = min(tmp_list)
            min_index = tmp_list.index(min_of_list)

            if min_of_list > 0.5:
                ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            else:
                ufi,lat,lon,country,lc=admin_res[min_index]
            print(ufi,lat,lon,country,lc,'222222',min_of_list)
            count_res_2 += 1


        update_sql='''update %s set geo_ufi=%s,lat=%s,lon=%s,fips_cc1='%s',lang_code='%s' where code ='%s' ''' % (table1,ufi,lat,lon,country,lc,code)
        print(update_sql)
        try:
            mysql_handle.set_sql(database,update_sql)
        except:
            print(ufi,lat,lon,country,lc)
            return
    print(count_res_0,count_res_1,count_res_2)


#对地级市（level = 2）进行匹配
def set_city():
    sql1 = '''SELECT code,a.level,a.name FROM %s a WHERE a.level = 2 ''' %(table1)
    result_area = mysql_handle.get_select(database,sql1)      #二重元组((,,),(,,),...)
    print len(result_area)

    count_res_0 = 0
    count_res_1 = 0
    count_res_2 = 0

    for i in range(len(result_area)):
    #for i in range(2):
        #逐条取result_area中的记录，并赋值
        item = result_area[i]                #(u'110100000000', 2L, u'\u5e02\u8f96\u533a')
        code = item[0]                       #area_change表中地级市代码：130100000000
        level = item[1]                      #area_change表中地级市级别：2
        name = item[2]                       #area_change表中地级市名称：石家庄市

        if name in city_black_list :
            name = ''

        #取result_area中地级市所在的省份
        prov = code[0:2]                     #地区所在省份：11   北京市

        #取出省份code在area_change表中对应的省份名称
        sql_get_prov_name = '''select name from %s where code = "%s" ''' %(table1,prov)
        prov_name = mysql_handle.get_select(database,sql_get_prov_name)[0][0]
        all_name = prov_name + name

        #取出code在provinces表中对应的adm1
        sql_get_prov_code = '''select adm1 from %s where code = "%s" ''' %(table3,prov)
        adm1 = mysql_handle.get_select(database,sql_get_prov_code)[0][0]               #get_select  ((u'22',),)

        #省份相同，级别相同，名称相同，从'ch_administrative_a'表提取相应信息
        sql2 = '''select ufi,lat,lon,cc1,lc from %s
                  WHERE adm1 = "%s" and substr(dsg,4,1) = "%s" and full_name_nd_ro = "%s" ''' %(table2,adm1,level,name)
        admin_res=mysql_handle.get_select(database,sql2)   #((-1903688L, u'39.932273', u'116.41002', u'CH', u'zho'),)
        admin_len=len(admin_res)            #判断是否有重复条数

        if admin_len == 0:
            print admin_res
            lat,lon = locate.get_coordinates(all_name)
            ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            print(ufi,lat,lon,country,lc,000000)
            count_res_0 += 1


        elif admin_len == 1:
            ufi,lat,lon,country,lc=admin_res[0]
           #print(ufi,lat,lon,country,lc,111111)
            count_res_1+=1

        else:
            lat,lon = locate.get_coordinates(all_name)              #google经纬度
            tmp_list = []                                           #与google经纬度差值
            for i in range(admin_len):
                item = admin_res[0]
                tmp_lat,tmp_lon = item[1],item[2]
                tmp_list.append(abs(lat - float(tmp_lat)) + abs(lon - float(tmp_lon)))
            min_of_list = min(tmp_list)
            min_index = tmp_list.index(min_of_list)

            if min_of_list > 0.5:
                ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            else:
                ufi,lat,lon,country,lc=admin_res[min_index]
            print(ufi,lat,lon,country,lc,'222222',min_of_list)
            count_res_2 += 1


        update_sql='''update %s set geo_ufi=%s,lat=%s,lon=%s,fips_cc1='%s',lang_code='%s' where code ='%s' ''' % (table1,ufi,lat,lon,country,lc,code)
        # print(update_sql)
        try:
            mysql_handle.set_sql(database,update_sql)
        except:
            print(ufi,lat,lon,country,lc)
            return
    print(count_res_0,count_res_1,count_res_2)


#对县级市（level = 3）进行匹配
def set_county():
    sql1 = '''SELECT code,a.level,a.name FROM %s a WHERE a.level = 3 ''' %(table1)
    result_area = mysql_handle.get_select(database,sql1)      #二重元组((,,),(,,),...)
    print len(result_area)

    count_res_0 = 0
    count_res_1 = 0
    count_res_2 = 0

    for i in range(len(result_area)):
    #for i in range(2):
        #逐条取result_area中的记录，并赋值
        item = result_area[i]                #3136
        code = item[0]                       #area_change表中地区代码：110101000000
        level = item[1]                      #area_change表中级别：3
        name = item[2]                       #area_change表中名称：东城区

        #取result_area中地区所在的省份和地级市
        prov = code[0:2]                     #地区所在省份：11   北京市
        city = code[0:4] + '00000000'        #地区所在地级市：110100000000    市辖区

        #取出省份code在area_change表中对应的省份名称
        sql_get_prov_name = '''select name from %s where code = "%s" ''' %(table1,prov)
        prov_name = mysql_handle.get_select(database,sql_get_prov_name)[0][0]

        #取出地市code在area_change表中对应的地市名称
        sql_get_city_name = '''select name from %s where code = "%s" ''' %(table1,city)
        city_name = mysql_handle.get_select(database,sql_get_city_name)[0][0]

        if city_name in city_black_list :
            city_name = ''
        if name in county_black_list :
            name = ''
        all_name = prov_name + city_name + name

        #取出code在provinces表中对应的adm1
        sql_get_prov_code = '''select adm1 from %s where code = "%s" ''' %(table3,prov)
        adm1 = mysql_handle.get_select(database,sql_get_prov_code)[0][0]               #get_select  ((u'22',),)

        #省份相同，级别相同，名称相同，从'ch_administrative_a'表提取相应信息
        sql2 = '''select ufi,lat,lon,cc1,lc from %s
                  WHERE adm1 = "%s" and substr(dsg,4,1) = "%s" and full_name_nd_ro = "%s" ''' %(table2,adm1,level,name)
        admin_res=mysql_handle.get_select(database,sql2)   #((-1903688L, u'39.932273', u'116.41002', u'CH', u'zho'),)
        admin_len=len(admin_res)            #判断是否有重复条数

        if admin_len == 0:
            lat,lon = locate.get_coordinates(all_name)
            ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            print(ufi,lat,lon,country,lc,000000)
            count_res_0 += 1

        elif admin_len == 1:
            ufi,lat,lon,country,lc=admin_res[0]
            print(ufi,lat,lon,country,lc,111111)
            count_res_1+=1

        else:
            lat,lon = locate.get_coordinates(all_name)              #google经纬度
            tmp_list = []                                           #与google经纬度差值
            for i in range(admin_len):
                item = admin_res[0]
                tmp_lat,tmp_lon = item[1],item[2]
                tmp_list.append(abs(lat - float(tmp_lat)) + abs(lon - float(tmp_lon)))
            min_of_list = min(tmp_list)
            min_index = tmp_list.index(min_of_list)

            if min_of_list > 0.5:
                ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            else:
                ufi,lat,lon,country,lc=admin_res[min_index]
            print(ufi,lat,lon,country,lc,'222222',min_of_list)
            count_res_2 += 1


        update_sql='''update %s set geo_ufi=%s,lat=%s,lon=%s,fips_cc1='%s',lang_code='%s' where code ='%s' ''' % (table1,ufi,lat,lon,country,lc,code)
        print(update_sql)
        try:
            mysql_handle.set_sql(database,update_sql)
        except:
            print(ufi,lat,lon,country,lc)
            return
    print(count_res_0,count_res_1,count_res_2)



if __name__ == "__main__":
    set_city()
    #set_county()
