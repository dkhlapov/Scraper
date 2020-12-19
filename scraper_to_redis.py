import json
import re
import urllib.request
from datetime import timedelta

import redis
from bs4 import BeautifulSoup


def redis_setup():
    r = redis.Redis(host='scraper_service', port=6379)
    link = urllib.request.urlopen("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(link, 'html.parser')
    hashes_raw = [a.string for a in
                  soup.find_all("a", class_="sc-1r996ns-0 gzrtQD sc-1tbyx6t-1 kXxRxe iklhnl-0 boNhIO d53qjk-0 jmTmMY")]
    bitcoin = [a.string[:-4].replace(',','') for a in soup.find_all("span", class_="sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg",
                                               string=re.compile(r'\d+,*\d*\.\d+ BTC'))]
    time = [a.string for a in soup.find_all("span", class_="sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg",
                                            string=re.compile(r'\d\d:\d\d'))]
    dollars = [a.string[1:].replace(',', '') for a in soup.find_all("span", class_="sc-1ryi78w-0 gCzMgE sc-16b9dsl-1 kUAhZx u3ufsr-0 fGQJzg",
                                               string=re.compile(r'\$\d+,*\d*\.\d+'))]
    d = {}
    for (item_hashes, item_time, item_btc, item_usd) in zip(hashes_raw, time, bitcoin, dollars):
        d[item_hashes] = {'time': item_time, 'btc': item_btc, 'usd': item_usd}
    with r.pipeline() as pipe:
        for hash, properties in d.items():
            pipe.hmset(hash, properties)
            pipe.expire(hash, timedelta(seconds=60))
        pipe.execute()
