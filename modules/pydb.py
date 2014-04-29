#!/usr/bin/python
# Filename: pydb.py

import MySQLdb
import MySQLdb.cursors

def runSQL(query):
    conn = MySQLdb.connect('localhost','root','password','sbs',cursorclass=MySQLdb.cursors.DictCursor)
    curs = conn.cursor()
    curs.execute(query)
    result = curs.fetchall()
    conn.commit()
    curs.close()
    return result
