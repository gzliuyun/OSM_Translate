#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'usr'

import sys
import mysql_handle
import mysql_crud_example
import google_coordinate as locate

def delete_non_chinese_char():
    database='area'
    sql=''
    mysql_handle.set_sql(database,sql)

# 把“村委会”结尾的名称改为“村”
# 吧“社区居委会”结尾的名称，改为社区
# 把“街道办事处”结尾的名称，改为街道

# mysql_handle.set_sql() 执行插入、删改
# mysql_handle.get_select() 查询

database='source'
table1 = 'area_change'
table2 = 'ch_administrative_a'
table3 = 'provinces'
city_black_list=[u'市辖区',u'县',u'河南省直辖县级行政区划',u'湖北省直辖县级行政区划',u'海南省直辖县级行政区划',u'新疆自治区直辖县级行政区划']
county_black_list=[u'市辖区']
#sql='select count(*) from %s' % (table)
#    a=mysql_handle.get_select(database,sql)


# def set_village():
#
#     sql = 'UPDATE `area_change` a SET a.`geo_ufi` = (SELECT b.`UFI`  FROM `ch_administrative_a` b WHERE a.`name` = b.`FULL_NAME_ND_RO` AND a.LEVEL  = 1)'
#     a= mysql_handle.set_sql(database,sql)
#     print(a)

#根据name对省份（level = 1）进行匹配
def set_province():
    sql = """UPDATE %s a SET a.`geo_ufi` =
          (SELECT b.`UFI`  FROM %s b WHERE a.`name` =
          b.`FULL_NAME_ND_RO` AND a.LEVEL  = 1)""" % (table1,table2)
    a = mysql_handle.set_sql(database,sql)
    print(a)

#根据name对地级市（level = 2）进行匹配
def set_city():
    #地级市名称相同，行政级别相同
    sql = '''UPDATE %s a SET a.`geo_ufi` = (SELECT DISTINCT b.`UFI` FROM %s b ,%s c
            WHERE a.`name` = b.`full_name_nd_ro`
            AND SUBSTR(a.code,1,2) = c.code AND b.adm1 = c.adm1
            AND a.`level` = 2 AND  SUBSTR(b.dsg,4,1) = '2') where a.geo_ufi is null''' % (table1,table2,table3)
    b = mysql_handle.set_sql(database,sql)

    #地级市名称相同，行政级别不同
    sql = '''UPDATE %s a SET a.`geo_ufi` = (SELECT DISTINCT b.`UFI` FROM %s b ,%s c
        WHERE a.`name` = b.`full_name_nd_ro`
        AND SUBSTR(a.code,1,2) = c.code AND b.adm1 = c.adm1
        AND a.`level` = 2 ) where a.geo_ufi is null''' % (table1,table2,table3)
    b = mysql_handle.set_sql(database,sql)
    print(b)

    #三沙市
    sql = '''UPDATE %s a SET a.lat = 16.8348569,a.lon = 112.3384975 where a.name='三沙市' ''' % (table1)
    b = mysql_handle.set_sql(database,sql)
    print(b)


#根据name对县级市（level = 3）进行匹配
def set_county():
    # #县级市名称相同，行政级别相同
    # sql = '''UPDATE %s a SET a.`geo_ufi` = (SELECT DISTINCT b.`UFI` FROM %s b ,%s c
    #         WHERE a.`name` = b.`full_name_nd_ro`
    #         AND SUBSTR(a.code,1,2) = c.code AND b.adm1 = c.adm1
    #         AND a.`level` = 3 AND  SUBSTR(b.dsg,4,1) = '3') where a.geo_ufi is null''' % (table1,table2,table3)
    # b = mysql_handle.set_sql(database,sql)
    #
    # #县级市名称相同，行政级别不同
    # sql = '''UPDATE %s a SET a.`geo_ufi` = (SELECT DISTINCT b.`UFI` FROM %s b ,%s c
    #     WHERE a.`name` = b.`full_name_nd_ro`
    #     AND SUBSTR(a.code,1,2) = c.code AND b.adm1 = c.adm1
    #     AND a.`level` = 3 ) where a.geo_ufi is null''' % (table1,table2,table3)
    # b = mysql_handle.set_sql(database,sql)
    # print(b)
    #
    # #三沙市
    # sql = '''UPDATE %s a SET a.lat = 16.8348569,a.lon = 112.3384975 where a.name='三沙市' ''' % (table1)
    # b = mysql_handle.set_sql(database,sql)
    # print(b)

    #area_change表中各记录
    sql1 = '''SELECT code,a.level,a.name FROM %s a WHERE a.level = 3 ''' %(table1)
    result_area = mysql_handle.get_select(database,sql1)
    count_res_1=0
    count_res_2=0
    count_res_0=0
    for i in range(len(result_area)) :
        item=result_area[i]
        code=item[0]
        prov=item[0][0:2]
        city=item[0][0:4]+'00000000'
        # print(prov)
        sql_get_prov_code=''' select adm1 from %s where code = %s ''' %(table3,prov)
        adm1=mysql_handle.get_select(database,sql_get_prov_code)[0][0]
        # print(adm1)
        level=item[1]
        name=item[2]
        sql2 = '''SELECT ufi,lat,lon,cc1,lc FROM %s where full_name_nd_ro="%s" and adm1= "%s" and substr(dsg,4,1)='%s' ''' %(table2,name,adm1,level)
        admin_res=mysql_handle.get_select(database,sql2)
        admin_len=len(admin_res)



        if admin_len==0:
            sql_get_prov_name=''' select name from %s where code = %s ''' %(table1,prov)
            prov_name=mysql_handle.get_select(database,sql_get_prov_name)[0][0]
            sql_get_city_name=''' select name from %s where code = %s ''' %(table1,city)
            city_name=mysql_handle.get_select(database,sql_get_city_name)[0][0]
            if city_name in city_black_list :
                city_name=''
            if name in county_black_list:
                name=''
            all_name=prov_name+city_name+name
            lat,lon=locate.get_coordinates(all_name)
            ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            print(ufi,lat,lon,country,lc,000000)
            count_res_0+=1

        elif admin_len==1:
            ufi,lat,lon,country,lc=admin_res[0]
            print(ufi,lat,lon,country,lc,111111)
            count_res_1+=1
        else:
            sql_get_prov_name=''' select name from %s where code = %s ''' %(table1,prov)
            prov_name=mysql_handle.get_select(database,sql_get_prov_name)[0][0]
            sql_get_city_name=''' select name from %s where code = %s ''' %(table1,city)
            city_name=mysql_handle.get_select(database,sql_get_city_name)[0][0]
            if city_name in city_black_list :
                city_name=''
            if name in county_black_list:
                name=''
            all_name=prov_name+city_name+name
            lat,lon=locate.get_coordinates(all_name)
            temp_list=[]
            for i in range(admin_len):
                item=admin_res[i]
                temp_lat,temp_lon=item[1],item[2]
                temp_list.append(abs(lat-float(temp_lat))+abs(lon-float(temp_lon)))
            min_of_list=min(temp_list)
            min_index=temp_list.index(min_of_list)
            if min_of_list>0.5:
                ufi,lat,lon,country,lc='NULL',lat,lon,'CH','zho'
            else:
                ufi,lat,lon,country,lc=admin_res[min_index]
            print(ufi,lat,lon,country,lc,'222222',min_of_list)
            count_res_2+=1

            # print(name)
        update_sql='''update %s set geo_ufi=%s,lat=%s,lon=%s,fips_cc1='%s',lang_code='%s' where code ='%s' ''' % (table1,ufi,lat,lon,country,lc,code)
        print(update_sql)
        try:
            mysql_handle.set_sql(database,update_sql)
        except:
            print(ufi,lat,lon,country,lc)
            return
    print(count_res_0,count_res_1,count_res_2)


    # print len(result_area)
    #
    #     #ch_administrative_a表中记录
    # sql2 = '''SELECT full_name_nd_ro,adm1 FROM %s where SUBSTR(dsg,4,1) = '3'  '''%(table2)
    # result_admi = mysql_handle.get_select(database,sql2)
    #
    # #provinces表中记录
    # sql3 = '''SELECT * FROM %s '''%(table3)
    # result_pro = mysql_handle.get_select(database,sql3)


    #area_change表中各记录
    # for i in range(len(result_area)) :
    #     print result_area[i]
    #     for j in range(len(result_area[i])):
    #         temp=result_area[i][j]
    #         if isinstance(temp,unicode)==False:
    #            temp=str(temp)
    #         print(temp)


    # mysql_crud_example.print_sql_res((result_area[1],))
    # print result_area[1]
    # print (result_area[1][1])



#     SELECT a.name,SUBSTR(a.code,1,2) CODE
# FROM `area_change` a,`ch_administrative_a` b ,provinces c
# WHERE a.`name` = b.`full_name_nd_ro`
#       AND SUBSTR(a.code,1,2) = c.code AND b.adm1 = c.adm1
#       AND a.`level` = 3 AND  SUBSTR(b.dsg,4,1) = '3'
# GROUP BY  a.name,SUBSTR(a.code,1,2)
# HAVING COUNT(*) = 1
# for line in result:
#     if line[1] not in dict:
#         print "error" + line[1]
#     dict[line[1]][106] = line[3]
#     dict[line[1]][112] = line[2]



if __name__ == "__main__":
    # print("陈")
    # a="长沙村委会12ba"
    # # print(a,len(a))
    # b=unicode(a,'utf-8')
    # print(b,len(b))
    # b=b.encode("GB18030")
    # print(b,len(b))
    # b=b.encode('gbk')
    # print(b,len(b))

    #set_province()
    #set_city()
    set_county()
