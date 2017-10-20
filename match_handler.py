# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 17:28:23 2017

@author: Marco
"""
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='matchs', charset='UTF8')
cursor = conn.cursor()