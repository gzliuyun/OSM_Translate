#!/usr/bin/python
# -*- coding:utf-8 -*-

import mysql_handle

# 简单sql增删
def delete_non_chinese_char():
    database='source'
    table='area_change'
    sql='增删语句'
    mysql_handle.set_sql(database,sql)

# 把“村委会”结尾的名称改为“村”
# 吧“社区居委会”结尾的名称，改为社区
# 把“街道办事处”结尾的名称，改为街道

#简单sql查询
def set_village():
    database='source'
    table='area_change'
    sql="""select * from %s where name like '%%长沙%%'""" % (table)
    # print(unicode(sql,'utf-8'))
    print(sql)
    a=mysql_handle.get_select(database,sql)
    print_sql_res(a)

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

if __name__ == "__main__":

    # print(a.encode('gb2312'))
    # print unicode(a,"utf-8")
    set_village()
