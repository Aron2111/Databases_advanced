import imp
import string
import pymongo
from pymongo import MongoClient
import redis
import time
import ast
conn = redis.Redis('localhost')



client = pymongo.MongoClient("mongodb://localhost:27017")
# database
db = client["bitcoin_data"]
# collection
collection= db["data"]
dblist = client.list_database_names()
if "bitcoin_data" in dblist:
  print("The database exists.")
else:
    print("dont exist")
    print(dblist)

while 1:
    BTC = 0
    data = {}

    for key in conn.scan_iter():
        key = str(key)[2:-1:]
        line = str(conn.get(key))[2:-1:]
        y = ast.literal_eval(line)
        if(y["BTC"]>BTC):
            BTC=y["BTC"]
            data=y
        conn.delete(key)

    try:
        if data!=" ":
            print("good")
            insert = collection.insert_one(data)
            print(data)
            data = {}
        else:
            pass
    except:
        pass
    time.sleep(60)

