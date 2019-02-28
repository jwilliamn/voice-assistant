#!/usr/bin/env python
# coding: utf-8

"""
    Show Room Assistant Client
    ============================================
    Free Poc:
    Trace detected person activity
    Give rewards for certain activity

    Note: 
    Structure:
    _copyright_ = 'Copyright (c) 2019 J.W. - Everis', 
    _license_ = GNU General Public License
"""

# Library
import mysql.connector
import pandas as pd

# variables de conexión
host_= "192.168.8.100"
user_="root"
passwd_="skynet123$"
database_="deepai"

# Líneas para conexión
conn = mysql.connector.connect(host=host_, user=user_, passwd=passwd_, database=database_)
cursor = conn.cursor()
df = pd.read_sql("SELECT * FROM sentiment2 ORDER BY time DESC LIMIT 500", conn)
print("database tail: ", df)

