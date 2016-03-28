#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update

$minimal_apt_get_install libpython3.5-dev python3.5-dev libffi-dev gcc build-essential autoconf libtool pkg-config libpq-dev
$minimal_apt_get_install libsqlite3-dev
$minimal_apt_get_install wget git

#DANGEROUS TO RENAME PYTHON
#rm -f /usr/bin/python
#rm -f /usr/bin/python3
#ln -s /usr/bin/python3.5 /usr/bin/python
#ln -s /usr/bin/python3.5 /usr/bin/python3


cd /tmp
rm -rf get-pip.py
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

pip install https://github.com/google/brotli/archive/master.zip
pip install https://github.com/jplana/python-etcd/archive/master.zip

pip install 'cython>=0.23.4' git+git://github.com/gevent/gevent.git#egg=gevent

pip install paramiko

pip install msgpack-python
pip install redis
pip install credis
pip install aioredis

pip install mongoengine

pip install bcrypt
pip install blosc
pip install certifi
pip install docker-py

pip install gitlab3
pip install gitpython
pip install html2text

# pip install pysqlite
pip install click
pip install influxdb
pip install ipdb
pip install ipython --upgrade
pip install jinja2
pip install netaddr

pip install reparted
pip install pytoml
pip install pystache
pip install pymongo
pip install psycopg2
pip install pathtools
pip install psutil

pip install pytz
pip install requests
pip install sqlalchemy
pip install urllib3
pip install zmq
pip install pyyaml
pip install websocket
pip install marisa-trie
pip install pylzma
pip install ujson
pip install watchdog
