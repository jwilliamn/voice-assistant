#!/usr/bin/env python
# coding: utf-8

# ### Interactive Assistant Client App

# Trace (track down) detected person actions

# """
#     Interactive Assistant Client
#     ============================================
#     Voice assistant client:
#     Give challenge to detected person
#     Give rewards for certain activity
# 
#     Note: 
#     Structure:
#     _copyright_ = 'Copyright (c) 2019 J.W. - Everis', 
#     _license_ = GNU General Public License
# """

# In[1]:


import mysql.connector
import pandas as pd
import re

import requests
import json
import time
from os.path import join


# In[2]:


# variables de conexión to DataBase
host_= "192.168.M.MMM" 
user_="db_user"
passwd_="db_user_password"
database_="database_name"


# In[ ]:


conn = mysql.connector.connect(host=host_, user=user_, passwd=passwd_, database=database_)
cursor = conn.cursor()
df = pd.read_sql("select * from sentiment2 where ddate = current_date() and time >= subtime(current_time(),000003) order by time DESC", conn)
df.head()


# In[4]:


list_detected = df["name"].value_counts()


# Lógica para detectar y verificar que el reto se está dando sobre la misma persona

# In[5]:


# Url service that interacts with current person in front of the screen
URL = "http://127.0.0.1:5000/"
ENDPOINT = join(URL, "test")
headers = {'Content-Type': 'application/json; charset=UTF-8'}


# In[6]:


# Sentiment detection
def detectSentiment(sentiment, name, reto):
    time.sleep(0)

    success = "No"
    timeout = time.time() + 3
    while time.time() < timeout:

        conn = mysql.connector.connect(host=host_, user=user_, passwd=passwd_, database=database_)
        cursor = conn.cursor()
        df = pd.read_sql("select * from sentiment2 where ddate = current_date() and time >= subtime(current_time(),000004) order by time DESC", conn)

        scores = list(df[sentiment][df["name"]==name])
        #print("scores: ", scores)
        
        if len(scores) > 0:
            if (max(scores) >= 0.6):
                score = "positive"
                reto = reto
                action = "input.feedback"
                success = "Yes"
                break
            else:
                score = "negative"
                reto = reto
                action = "input.feedback"
                success = "No"
        else:
            score = "negative"
            reto = reto
            action = "input.terminate"
            success = "No"
            
    return success, score, reto, action


# In[7]:


# Check current person
def checkCurrentPerson(currentName):
    stillthere = "No"
    timeout = time.time() + 1
    while time.time() < timeout:

        conn = mysql.connector.connect(host=host_, user=user_, passwd=passwd_, database=database_)
        cursor = conn.cursor()
        df = pd.read_sql("select * from sentiment2 where ddate = current_date() and time >= subtime(current_time(),000004) order by time DESC", conn)

        list_detected = df["name"].value_counts()
        
        if list_detected.count() > 0:
            names = list(list_detected.index)
            if currentName in names:
                stillthere = "Yes"
                break
        else: stillthere = "No"
            
    return stillthere


# In[8]:


# Only interact with the ones that have real names (not ID_43)
def notRealName(inputString):
    return bool(re.search(r'\d', inputString))


# In[ ]:


# Real time connection to DB
detected = "No"

action = 'input.welcome'
name = ""
score = ""
reto = ""
state = ""

session = "end"

repeat = 0
fail = 0
listReto = []

# Interaction mode 1=Presentation and 0=Development
interaction_mode = 1
completed_challenge = []

while True:
    if session == "end" and detected == "No":
        conn = mysql.connector.connect(host=host_, user=user_, passwd=passwd_, database=database_)
        cursor = conn.cursor()
        df = pd.read_sql("select * from sentiment2 where ddate = current_date() and time >= subtime(current_time(),000003) order by time DESC", conn)
        
        list_detected = df["name"].value_counts()
        
        if list_detected.count() > 0:
            curr_names = list(list_detected.index)
            name = ""
            for i in range(len(curr_names)):
                if notRealName(curr_names[i]):
                    pass
                else:
                    if interaction_mode == 1:
                        if curr_names[i] not in completed_challenge:
                            name = curr_names[i]
                            break
                        else: pass
                    else:
                        name = curr_names[i]
                        break
            
            if name != "":
                detected = "Yes"
                action = "input.welcome"
                repeat = 0
                fail = 0
                listReto = []
            else: detected = "No"
        else: detected = "No"
    else:
        data = json.dumps({'name':name, 'action':action, 'score':score, 'reto':reto, 'repeat':repeat, 'fail':fail, 
                           'listReto':listReto, 'session':session}).encode('utf-8')
        response = requests.post(ENDPOINT, headers = headers, data=data)
        result = response.json()
        print("Result:", result)
        
        session = result['fulfillmentText']['session']
        detected = result['fulfillmentText']['detected']
        state = result['fulfillmentText']['state']
        
        if state == "welcome":
            #time.sleep(1)
            stillthere = checkCurrentPerson(name)
            if stillthere == "Yes":
                action = "input.challenge"
            else:
                action = "input.terminate"
        
        if state == "challenge":
            reto = result['fulfillmentText']['reto']
            if reto == "happiness":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
                        
            elif reto == "surprise":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
            
            elif reto == "sadness":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
            
            elif reto == "anger":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
            
            elif reto == "disgust":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
            
            elif reto == "fear":
                sentiment = reto
                listReto.append(reto)
                succ, score, reto, action = detectSentiment(sentiment, name, reto)
                if succ == "Yes":
                    repeat += 1
                else: fail += 1
            else: pass
        
        if state == "terminate":
            time.sleep(10)
            pass
        
        if state == "completed":
            completed_challenge.append(name)
            pass

