#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb

conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test', port=3306)
cur = conn.cursor()
cur.execute('select * from testtable')
for row in cur.fetchall():
    print row
cur.close()
conn.close()



