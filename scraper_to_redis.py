import json
import re
import urllib.request
from datetime import timedelta

import redis
from bs4 import BeautifulSoup


def redis_setup():
    r = redis.Redis(host='172.26.0.4', port=6379)
    link = urllib.request.urlopen("https://www.blockchain.com/btc/unconfirmed-transactions")
    soup = BeautifulSoup(link, 'html.parser')
    hashes_raw = [a.string for a in
                  soup.find_all("a", class_="sc-1r996ns-0 fLwyDF sc-1tbyx6t-1 kCGMTY iklhnl-0 eEewhk d53qjk-0 ctEFcK")]
    bitcoin = [a.string[:-4].replace(',','') for a in soup.find_all("span", class_="sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC",
                                               string=re.compile(r'\d+,*\d*\.\d+ BTC'))]
    time = [a.string for a in soup.find_all("span", class_="sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC",
                                            string=re.compile(r'\d\d:\d\d'))]
    dollars = [a.string[1:].replace(',', '') for a in soup.find_all("span", class_="sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC",
                                               string=re.compile(r'\$\d+,*\d*\.\d+'))]
    d = {}
    for (item_hashes, item_time, item_btc, item_usd) in zip(hashes_raw, time, bitcoin, dollars):
        d[item_hashes] = {'time': item_time, 'btc': item_btc, 'usd': item_usd}
    with r.pipeline() as pipe:
        for hash, properties in d.items():
            pipe.hmset(hash, properties)
            pipe.expire(hash, timedelta(seconds=60))
        pipe.execute()
