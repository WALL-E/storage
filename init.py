#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('data.db')

print "Opened database successfully"

conn.execute('''CREATE TABLE data
               (timestamp INT NOT NULL,
                text TEXT NOT NULL,
                filename CHAR(128));''')

print "Table created successfully"

conn.close()
