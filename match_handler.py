# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:28:23 2017

@author: Marco
"""
import misc
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
cursor = conn.cursor()

matchStr = misc.getOneMatchDetail(conn,cursor)
#matchStr[0]为id，matchStr[1]为simple，matchStr[2]为detail

simpleStr = matchStr[1].replace('["','').replace('"]','')
simpleList = simpleStr.split('","')
print(simpleList)

match = []
match.append(simpleList[0])#id
match.append(simpleList[2])#league
match.append(str(simpleList[43])+'-'+str(simpleList[36])+' '+ str(simpleList[11])+':00')#time
match.append(simpleList[5])#home
match.append(simpleList[8])#guest
match.append(simpleList[14])#home_goal
match.append(simpleList[15])#guest_goal
match.append(simpleList[16])#home_goal_h
match.append(simpleList[17])#guest_goal_h
match.append(simpleList[29])#point
match.append(simpleList[46])#goals
match.append(simpleList[48])#home_corner
match.append(simpleList[49])#guest_corner
match.append(simpleList[18])#home_red
match.append(simpleList[19])#guest_red
match.append(simpleList[20])#home_yellow
match.append(simpleList[21])#guest_yellow
print(match)