sudo apt-get install tcl
sudo apt-get install gcc
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
cd src
sudo apt-get install redis-server
redis-server