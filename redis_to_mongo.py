import pymongo as mongo

from scraper_to_redis import redis_setup

client = mongo.MongoClient("mongodb://127.0.0.1:27017")
scraper_db = client['scraper']
col_hashes = scraper_db['hashes']
redis_setup()
