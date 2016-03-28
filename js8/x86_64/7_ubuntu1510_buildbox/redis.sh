#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

# groupadd -r redis && useradd -r -g redis redis

# $minimal_apt_get_install build-essential
$minimal_apt_get_install wget tar

mkdir -p /opt/redis
cd /opt/redis
wget http://download.redis.io/releases/redis-3.0.6.tar.gz
tar xzf redis-3.0.6.tar.gz
cd redis-3.0.6

# rm -rf /build/opt/redis
# mkdir -p /build/opt/redis
# rm -rf /build/optvar/redis/
# mkdir -p /build/optvar/redis/

rm -f /usr/local/bin/redis-server
rm -f /usr/local/bin/redis-cli
cp /opt/redis/redis-3.0.6/src/redis-server /opt/jumpscale8/bin/
cp /opt/redis/redis-3.0.6/src/redis-cli /opt/jumpscale8/bin/

mkdir -p /optvar/cfg/
cp /bd_build/redis.conf /optvar/cfg/

rm -rf /opt/redis