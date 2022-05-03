from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import quandl
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
# database
db = client["bitcoin"]
# collection
collection= db["test"]

starttime = time.time()
hash_list = []
time_list=[]
btc_list=[]
dollar_list=[]
#als je een for loop gebruikt of geen loop krijg je output maar doordat het blijft draaien krijg je die niet

html_tekst=requests.get('https://www.blockchain.com/btc/unconfirmed-transactions').text
soup=BeautifulSoup(html_tekst,"html.parser")
lijn=soup.find_all('div',class_='sc-1g6z4xm-0 hXyplo')



for result in lijn:
    lijn_hash=result.find('a',class_="sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK").text
    lijn_time=result.find_all('span',class_='sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC')
    x=(lijn_time[1].text.replace(' BTC',''))
    x=float(x)
    if(lijn_hash not in hash_list):
        hash_list.append(lijn_hash)
        time_list.append(lijn_time[0].text)
        btc_list.append(x)
        dollar_list.append(lijn_time[2].text)

df = pd.DataFrame(list(zip(hash_list, time_list,btc_list,dollar_list)),
            columns =['Hash', 'time','BTC','Dollar'])
df=df.sort_values(by=['BTC'],ascending=False)
print("Updated dataframe")
test=df.to_dict('records')
collection.insert_many(test)
