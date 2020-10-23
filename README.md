# Scraper

mongo_setup.bash - setting up mongodb on Ubuntu 20.04.1

scraper.py - scraping hashes info from blockchain.com every minute and storing the highest value hash in a mongodb database

# Usage

1. Check that both files are in the same repository
2. In bash terminal type:

	mongo_setup
	
	python3 scraper.py
