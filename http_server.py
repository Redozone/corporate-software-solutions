#! /usr/bin/python3
# coding: utf-8

# ./http_server.py config.json

from typing import Optional
import uvicorn
from fastapi import Request, FastAPI
from time import time

import os
import sys
from sys import argv
import json
import subprocess
import random

import psycopg2 # pip install psycopg2-binary
import http.client
   
print("4islo http server greets You!")   
    
conf_path = argv[1]
config = {}
with open(conf_path, 'r') as json_file:
    config = json.load(json_file)

host = config['host']
port = int(config['port'])
start = int(config['start'])
end = int(config['end'])

db_host = config['db_host']
db_user = config['db_user']
db_password = config['db_password']
db_name = config['db_name']
db_port = config['db_port']

number = 0

app = FastAPI()


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
    
connection = create_connection(db_name, db_user, db_password, db_host, db_port)

def insert(my_number, name):
    global connection
    conn = connection
    
    query = 'INSERT INTO vlad.random4 (ip, \"number\") VALUES (\''+str(name)+'\', '+str(my_number)+');'
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query)
    #https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27 
    
def select_history(connection, user_host):
    cursor = connection.cursor()
    result = None
    query = "SELECT \"number\" FROM vlad.random4 where ip = \'" + str(user_host) + "\' order by id desc limit 10;"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        
def my_love(connection, user_host):
    cursor = connection.cursor()
    result = None
    query = "select t1.number /*,t1.total*/ from (SELECT number, count(*) as total FROM vlad.random4 WHERE ip = \'"+ str(user_host) +"\' GROUP BY number) t1 where t1.total = (select max(t2.total) from (SELECT number, count(*) as total FROM vlad.random4 WHERE ip = \'"+ str(user_host) +"\' GROUP BY number) t2) limit 1;"
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# curl --header "Content-Type: application/json" --request PUT --data '{"start": "11", "end": "100"}' 192.168.34.65:9966/set_range
@app.put("/set_range")
async def write_json_policy(request: Request):
    global start, end, conf_path, config
    server_answer = {}
    try: 
        server_answer = await request.json()
    except:
        pass
    
    if (end > start):
        start = int(server_answer["start"])
        end = int(server_answer["end"])
        config["start"] = start
        config["end"] = end
        
        with open(conf_path, 'w') as json_conf:
           json.dump(config, json_conf, ensure_ascii=False, indent=4)

# curl -XGET 192.168.34.65:9966/love/vlad   
@app.get("/love/{name}")
def give_love(name: str):
    global connection
    love = my_love(connection, str(name))
    return {"love" : str(love)}

# curl -XGET 192.168.34.65:9966/history/vlad   
@app.get("/history/{name}")
def give_history(name: str):
    global connection
    numbs = select_history(connection, str(name))
    return {"history" : numbs}

# curl -XGET 192.168.34.65:9966/random/vlad   
@app.get("/random/{name}")
def do_random(name: str):
    global start, end
    rand = random.randint(int(start), int(end))
    number = rand
    insert(rand, str(name))
    return {"value" : str(rand)}

if __name__ == '__main__':
    uvicorn.run(app, port=port, host=host)

    
