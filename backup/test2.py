#!/usr/bin/python
# -*- coding:utf-8 -*-

import MySQLdb

try:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='test', port=3306)
    cur = conn.cursor()
    cur.execute('select * from testtable')
    for row in cur.fetchall():
        print row
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
