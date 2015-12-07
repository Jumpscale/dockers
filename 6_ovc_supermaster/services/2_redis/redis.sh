#!/bin/bash
set -e
source /code/buildconfig
set -x

groupadd -r redis && useradd -r -g redis redis

$minimal_apt_get_install build-essential

rm -rf /opt/redis
mkdir /opt/redis
cd /opt/redis
wget http://download.redis.io/releases/redis-3.0.5.tar.gz
tar xzf redis-3.0.5.tar.gz
cd redis-3.0.5
make

rm -f /usr/local/bin/redis-server
rm -f /usr/local/bin/redis-cli
ln /opt/redis/redis-3.0.5/src/redis-server /usr/local/bin/redis-server
ln /opt/redis/redis-3.0.5/src/redis-cli /usr/local/bin/redis-cli


mkdir -p /data/db && chown -R redis:redis /data/db

mkdir -p /build/redis
cp /usr/local/bin/redis* /build/redis

#mkdir /etc/service/redis
#cp /code/services/redis/redis.runit /etc/service/redis/run

#mkdir /etc/redis
#cp /code/services/redis/redis.conf /etc/redis/
