# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:41:27 2017

@author: Marco
"""
import re

def getOneMatchDetail(conn, cursor):
    sql = 'select id, simple, detail from match_detail limit 0, 1'
    cursor.execute(sql)
    matchStr = cursor.fetchone()#取一条，fetchall()取所有
    #matchStr[0]为id，matchStr[1]为simple，matchStr[2]为detail
    return matchStr

def getMatch(matchStr):
    simpleStr = matchStr[1].replace('["','').replace('"]','')#获取simple字段部分
    simpleList = simpleStr.split('","')
    match = []
    match.append(int(simpleList[0]))#id
    match.append(simpleList[2])#league
    match.append(str(simpleList[43])+'-'+str(simpleList[36])+' '+ str(simpleList[11])+':00')#time
    match.append(simpleList[5])#home
    match.append(simpleList[8])#guest
    match.append(int(simpleList[14]))#home_goal
    match.append(int(simpleList[15]))#guest_goal
    match.append(int(simpleList[16]))#home_goal_h
    match.append(int(simpleList[17]))#guest_goal_h
    match.append(float(simpleList[29]))#point
    match.append(float(simpleList[46]))#goals
    match.append(int(simpleList[48]))#home_corner
    match.append(int(simpleList[49]))#guest_corner
    match.append(int(simpleList[18]))#home_red
    match.append(int(simpleList[19]))#guest_red
    match.append(int(simpleList[20]))#home_yellow
    match.append(int(simpleList[21]))#guest_yellow
    return match

def getCompanyList(conn, cursor, matchStr):
    companyList = []
    companyMap = {}
    gamesStr = matchStr[2]#获取detail字段部分
    gamesList = re.findall(r'var game=Array\(\"(.*?)\"\);',gamesStr)[0].split('","')
    for game in gamesList:
        gameList = game.split('|')
        #print(gameList)
        companyMap[gameList[1]]=gameList[0]
        selectSql = 'select company_id from company where company_id = %s'
        cursor.execute(selectSql,gameList[0])
        if not cursor.fetchone():
            company=[]
            company.append(gameList[0])#company_id
            company.append(gameList[2])#company_name
            if re.findall(r'\((.*?)\)',gameList[21]):
                company.append(re.findall(r'\((.*?)\)',gameList[21])[0])#company_country
            else:
                company.append('')
            companyList.append(company)
    return companyList, companyMap

def getOddsList(matchStr, companyMap):
    matchId = matchStr[1].replace('["','').replace('"]','').split('","')[0]
    year = matchStr[1].replace('["','').replace('"]','').split('","')[43]
    gameDetailsStr = matchStr[2]#获取detail字段部分
    gameDetailsList = re.findall(r'gameDetail=Array\(\"(.*?)\"\);',gameDetailsStr)[0].split('","')
    oddsList = []
    for gameDetails in gameDetailsList:
        subCompanyId = re.findall(r'(.*?)\^',gameDetails)[0]
        gameDetailList = gameDetails.split('^')[1].split(';')
        for gameDetail in gameDetailList:
            if gameDetail == '':
                continue
            tempList = gameDetail.split('|')
            odds = []
            odds.append(matchId)
            odds.append(companyMap[subCompanyId])
            odds.append(year+'-'+tempList[3]+':00')
            odds.append(tempList[0])
            odds.append(tempList[1])
            odds.append(tempList[2])
            odds.append(tempList[4])
            odds.append(tempList[5])
            odds.append(tempList[6])
            oddsList.append(odds)
    return oddsList

def checkAndDeleteMatchDetail(conn, cursor, matchId):
    matchSelectSql = 'select match_id from `match` where match_id = %s'
    cursor.execute(matchSelectSql, matchId)
    if cursor.fetchone():
        matchDetailDeleteSql = 'delete from match_detail where id = %s'
        cursor.execute(matchDetailDeleteSql, matchId)
        conn.commit()
        return True
    return False