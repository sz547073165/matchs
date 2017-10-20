# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:41:27 2017

@author: Marco
"""

def getOneMatchDetail(conn, cursor):
    sql = 'select id, simple, detail from match_detail limit 0, 1'
    cursor.execute(sql)
    match = cursor.fetchone()#取一条，fetchall()取所有
    return match