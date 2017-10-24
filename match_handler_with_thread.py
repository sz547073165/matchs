# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 13:22:51 2017

@author: Marco
"""

import misc
import pymysql
import threading
import time

matchInsertSql = 'insert into `match` (match_id, league, time, home, guest, home_goal, guest_goal, home_goal_h, guest_goal_h, points, goals, home_corner, guest_corner, home_red, guest_red, home_yellow, guest_yellow) '
matchInsertSql += 'value (%s, "%s", "%s", "%s", "%s", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'
companyInsertSql = 'insert into company (company_id, company_name, company_country) value (%s, "%s", "%s")'
oddsInsertSql = 'insert into odds (match_id, companys_id, time, win, draw, lose, k_win, k_draw, k_lose) value (%s, %s, "%s", %s, %s, %s, %s, %s, %s)'

'''初始化数据库连接'''
conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
cursor = conn.cursor()
'''获取10条match_detail'''
match_list = misc.get_ten_match_detail(conn, cursor)
sql_list = set()

class my_thread(threading.Thread):
    def __init__(self, thread_name, match):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.match = match
    def run(self):
        print('%s开始，，，\n'% self.thread_name)
        one_match_handler(self.match)
        print('%s结束，，，\n'% self.thread_name)

def one_match_handler(match):
    sub_conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
    try:
        match_id = match[0]
        print('matchId=%s\n'%match_id)
        is_exists = misc.check_match_detail(sub_conn, sub_conn.cursor(), match_id)
        if is_exists:
            sql_list.add(is_exists)
        else:
            match_obj = misc.getMatch(match)#获取match
            company_list, company_map = misc.getCompanyList(sub_conn, sub_conn.cursor(), match)#获取company列表
            odds_list = misc.getOddsList(match, company_map)#获取所有odds
            sql_list.add(matchInsertSql % tuple(match_obj))
            for company in company_list:
                sql_list.add(companyInsertSql % tuple(company))
            for odds in odds_list:
                sql_list.add(oddsInsertSql % tuple(odds))
    finally:
        sub_conn.close()
        
thread_list = []
for i in range(len(match_list)):
    thread_list.append(my_thread('thread-%s'%i, match_list[i]))

for thread in thread_list:
    thread.start()
for thread in thread_list:
    thread.join()

time.sleep(0.1)
print(len(sql_list))

for sql in sql_list:
    cursor.execute(sql)

try:
    conn.commit()
    print('success')
except:
    conn.rollback()
    print('fail')
conn.close()

print('end\n')