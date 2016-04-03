#!/usr/bin/python
# -*- coding:utf-8 -*-
"""CMySql类，简单的MySQL增删改查"""

import os.path
try:
    import MySQLdb
except ImportError:
    raise ImportError("[E]: MySQLdb module not found!")

class CMySql(object):
    def __init__(self):
        self.Option = {"host" : "", "password" : "", "username" : "", "database" : "","port" : ""}
    
    def setoptions(self, host, pwd, user, db,port):
        self.Option["host"] = host
        self.Option["password"] = pwd
        self.Option["username"] = user
        self.Option["database"] = db
        self.Option["port"]=port
    
    def start(self,fun,sqlstate,params=()):
        try:
            self.db = MySQLdb.connect(
                        host = self.Option["host"],
                        user = self.Option["username"],
                        passwd = self.Option["password"],
                        db = self.Option["database"],
                        port = self.Option["port"],
                        charset="utf8"
            )
            return fun(sqlstate,params)
        except Exception, e:
            # print e
            raise Exception("[E] Cannot connect to %s" % self.Option["host"])
        finally:
            try:
                self.close()
            except Exception, e:
                pass

    def create(self, sqlstate,param=()):
        """
        @todo: sqlstate可以自己改成其他参数，下同
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(sqlstate,param) #创建
        self.db.commit()


    def insert(self, sqlstate,param=()):
        """
        @todo: 虽然函数名是insert，不过增删改都行
        """
        self.cursor = self.db.cursor()
        self.cursor.execute(sqlstate,param) #增、删、改
        self.db.commit()

    def query(self, sqlstate,param=()):
        self.cursor = self.db.cursor()
        self.cursor.execute(sqlstate,param) #查
        qres = self.cursor.fetchall()
        return qres
    
    def one_query(self, sqlstate,param=()):
        self.cursor = self.db.cursor()
        self.cursor.execute(sqlstate,param) #查
        qres = self.cursor.fetchall()[0]
        return qres
        
    def close(self):
        self.db.close()

# 通过sql语句得到select结果
def get_select(database_name,sqlstate,params=()):
    cm=CMySql()
    import ConfigParser
    config=ConfigParser.ConfigParser()
    file_dir=os.path.dirname(os.path.abspath(__file__))
    config.read(file_dir+"/db.ini")
    host = config.get("db", "db_host")
    port = int(config.get("db", "db_port"))
    user = config.get("db", "db_user")
    pwd = config.get("db", "db_pass")
    # print(host,port,user,pwd)
    cm.setoptions(host=host,pwd=pwd,user=user,db=database_name,port=port)
    return cm.start(cm.query,sqlstate,params)

# 通过sql语句执行删改
def set_sql(database_name,sqlstate,params=()):
    cm=CMySql()
    import ConfigParser
    config=ConfigParser.ConfigParser()
    file_dir=os.path.dirname(os.path.abspath(__file__))
    config.read(file_dir+"/db.ini")
    host = config.get("db", "db_host")
    port = int(config.get("db", "db_port"))
    user = config.get("db", "db_user")
    pwd = config.get("db", "db_pass")
    # print(host,port,user,pwd)
    cm.setoptions(host=host,pwd=pwd,user=user,db=database_name,port=port)
    cm.start(cm.insert,sqlstate,params)
    return

#得到指定数据库的table结构，大写表示
def get_table_head(database_name):
    table_head_li=get_select(database_name,"show columns from "+database_name+"template")
    temp_li=[]
    for li in table_head_li:
        temp_li.append(li[0].upper())
    return temp_li
