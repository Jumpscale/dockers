#!/bin/bash
set -e
source /code/buildconfig
set -x

cd /tmp
curl -L  https://github.com/coreos/etcd/releases/download/v2.2.2/etcd-v2.2.2-linux-amd64.tar.gz -o etcd-v2.2.2-linux-amd64.tar.gz
tar xzvf etcd-v2.2.2-linux-amd64.tar.gz
cd etcd-v2.2.2-linux-amd64
mv etcd /usr/bin/
mv etcdctl /usr/bin/
cd ..
rm -rf etcd-v2.2.2-linux-amd64
rm -f etcd-v2.2.2-linux-amd64.tar.gz

mkdir -p /build/etcd
cp /usr/bin/etcd* /build/etcd/

#mkdir /etc/service/etcd
#cp /code/services/1_etcd/etcd.runit /etc/service/etcd/run
