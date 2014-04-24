#!/usr/bin/python
# Filename: pydb.py

import MySQLdb

def runSQL(query):
    conn = MySQLdb.connect('localhost','root','password','gpio')
    curs = conn.cursor()
    curs.execute(query)
    result = curs.fetchall()
    conn.commit()
    curs.close()
    return result
