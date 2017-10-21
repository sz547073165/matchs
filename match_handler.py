# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:28:23 2017

@author: Marco
"""
import misc
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
cursor = conn.cursor()
matchSelectSql = 'select count(*) from `match` where match_id = %s'
matchInsertSql = 'insert into `match` (match_id, league, time, home, guest, home_goal, guest_goal, home_goal_h, guest_goal_h, points, goals, home_corner, guest_corner, home_red, guest_red, home_yellow, guest_yellow) '
matchInsertSql += 'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
companyInsertSql = 'insert into company (company_id, company_name, company_country) value (%s, %s, %s)'
oddsInsertSql = 'insert into odds (match_id, companys_id, time, win, draw, lose, k_win, k_draw, k_lose) value (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
matchDetailDeleteSql = 'delete from match_detail where id = %s'
isNext = True
while isNext:
    matchStr = misc.getOneMatchDetail(conn,cursor)
    if not matchStr:
        isNext = False
        break
    '''if misc.checkAndDeleteMatchDetail(conn,cursor,matchStr[0]):
        continue'''
    print('matchId='+str(matchStr[0]))
    match = misc.getMatch(matchStr)#获取match
    companyList, companyMap = misc.getCompanyList(conn, cursor,matchStr)#获取company列表
    oddsList = misc.getOddsList(matchStr, companyMap)#获取所有odds
    try:
        cursor.execute(matchInsertSql, match)
        for company in companyList:
            cursor.execute(companyInsertSql, company)
        for odds in oddsList:
            cursor.execute(oddsInsertSql, odds)
        cursor.execute(matchDetailDeleteSql, matchStr[0])
        conn.commit()
    except:
        conn.rollback()
        print('fail')
cursor.close
conn.close