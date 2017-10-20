# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:28:23 2017

@author: Marco
"""
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
cursor = conn.cursor()

def getOneMatchDetail(conn, cursor):
    sql = 'select id, simple, detail from match_detail limit 0, 1'
    cursor.execute(sql)
    match = cursor.fetchone()#取一条，fetchall()取所有
    return match

match = getOneMatchDetail(conn,cursor)
print(match)