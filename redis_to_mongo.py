import pymongo as mongo
import redis
from scraper_to_redis import redis_setup

r = redis.Redis()
client = mongo.MongoClient("mongodb://127.0.0.1:27017")
scraper_db = client['scraper']
col_hashes = scraper_db['hashes']
redis_setup()
