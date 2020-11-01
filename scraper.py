import time as tm
import urllib.request

import pymongo as mongo
from bs4 import BeautifulSoup

client = mongo.MongoClient("mongodb://127.0.0.1:27017")
scraper_db = client['scraper']
col_hashes = scraper_db['hashes']
while True:
    link = urllib.request.urlopen("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(link, 'html.parser')
    hashes_raw = soup.find_all("a", class_="sc-1r996ns-0 gzrtQD sc-1tbyx6t-1 kXxRxe iklhnl-0 boNhIO d53qjk-0 jmTmMY")
    info = soup.find_all("span", class_="sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg")
    pos = 0
    maxusd = 0
    hashes, time, btc, usd = ([] for i in range(4))
    for i in range(len(info)):
        if ((i % 3 == 2) and (float(info[i].string[1:].replace(",", "")) > maxusd)):
            pos = i
            maxusd = float(info[i].string[1:].replace(",", ""))
    tophash = hashes_raw[pos // 3].string
    topusd = maxusd
    toptime = info[pos - 2].string
    topbtc = float(info[pos - 1].string[:-3].replace(",", ""))
    print(tophash, topusd, toptime, topbtc)
    d = {'hash': tophash, 'time': toptime, 'btc': topbtc, 'usd': topusd}
    insert_hash = col_hashes.insert_one(d)
    tm.sleep(60)
