#!/bin/bash
set -e
source /code/buildconfig
set -x

groupadd -r redis && useradd -r -g redis redis

$minimal_apt_get_install build-essential

mkdir /opt/redis
cd /opt/redis
wget http://download.redis.io/releases/redis-3.0.5.tar.gz
tar xzf redis-3.0.5.tar.gz
cd redis-3.0.5
make

ln /opt/redis/redis-3.0.5/src/redis-server /usr/local/bin/redis-server
ln /opt/redis/redis-3.0.5/src/redis-cli /usr/local/bin/redis-cli


mkdir -p /data/db && chown -R redis:redis /data/db


mkdir /etc/service/redis
cp /code/services/redis/redis.runit /etc/service/redis/run

mkdir /etc/redis
cp /code/services/redis/redis.conf /etc/redis/
