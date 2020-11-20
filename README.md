# Scraper
## Purpose
This scraper is made as an assignment at Thomas More University of Applied Sciences for the Databases Advanced course. The purpose of this scraper is to scrape the highest transactions by value from https://www.blockchain.com/btc/unconfirmed-transactions, cache them and store them in a NoSQL database.

## Prerequisites
Ubuntu 20.04.1 with python3 installed

## Files

mongo_setup.bash - setting up MongoDB on Ubuntu 20.04.1

redis_setup.bash - setting up Redis on Ubuntu 20.04.1

scraper_to_redis.py - scraping hashes info from blockchain.com and caches it in a Redis key-value database. The keys are set to expire every minute.

redis_to_mongo.py - the main script. Gets the values from Redis, sorts the values, takes the highest and puts it in a MongoDB every minute.

## Usage

1. Check that all the files are in the same repository
2. In bash terminal type:

	mongo_setup.bash
	
	redis_setup.bash
	
	python3 redis_to_mongo.py
