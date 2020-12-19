import pymongo as mongo
import redis
from scraper_to_redis import redis_setup
import time

r = redis.Redis(host='172.17.0.2', port=6379)
client = mongo.MongoClient("mongodb://127.0.0.1:27017")
scraper_db = client['scraper']
col_hashes = scraper_db['hashes']

def get_values(keys):
    pipe = r.pipeline()
    for key in keys:
        pipe.hgetall(key)
    values = pipe.execute()
    values = [{key.decode('utf-8'):value.decode('utf-8') for key,value in d.items()} for d in values]
    d = dict(zip(keys, values))
    d = {key.decode('utf-8'):value for key, value in d.items()}
    return d
while True:
    redis_setup()
    keys = r.keys()
    col_hashes.insert_one(dict(list(sorted(get_values(keys).items(), key=lambda x: float(x[1]["usd"]), reverse=True))[:1]))
    time.sleep(60)
