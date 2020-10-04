from bs4 import BeautifulSoup
import urllib.request
import numpy as np
import pandas as pd
import time as tm
import logging

df_final = pd.DataFrame()
FORMAT = 'Hash: %(hash)s Time: %(time)s BTC: %(btc)f USD: %(usd)f'
logging.basicConfig(filename="tophashes.log", level=logging.INFO, format=FORMAT, filemode='w')
logger = logging.getLogger()
while True:
    link = urllib.request.urlopen("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(link, 'html.parser')
    hashes_raw = soup.find_all("a", class_="sc-1r996ns-0 gzrtQD sc-1tbyx6t-1 kXxRxe iklhnl-0 boNhIO d53qjk-0 jmTmMY")
    info = soup.find_all("span", class_="sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg")
    hashes, time, btc, usd = ([] for i in range(4))
    for i in range(len(info)):
        if (i % 3 == 0):
            time.append(info[i].string)
        if (i % 3 == 1):
            btc.append(float(info[i].string[:-3].replace(",", "")))
        if (i % 3 == 2):
            usd.append(float(info[i].string[1:].replace(",", "")))
    for row in hashes_raw:
        hashes.append(row.string)
    dict = {'hash': hashes, 'time': time, 'btc': btc, 'usd': usd}
    df = pd.DataFrame(data=dict)
    df = df.sort_values(by='usd', ascending=False)
    records = df.head(1).to_dict('records')
    d = records[0]
    #df_final = df_final.append(df.head(1))
    logger.info('', extra=d)
    tm.sleep(60)
#print(df_final)
