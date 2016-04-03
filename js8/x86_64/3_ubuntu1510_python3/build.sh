#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update

$minimal_apt_get_install libpython3.5-dev python3.5-dev libffi-dev gcc build-essential autoconf libtool pkg-config libpq-dev
$minimal_apt_get_install libsqlite3-dev
$minimal_apt_get_install wget
$minimal_apt_get_install git



#DANGEROUS TO RENAME PYTHON
#rm -f /usr/bin/python
#rm -f /usr/bin/python3
#ln -s /usr/bin/python3.5 /usr/bin/python
#ln -s /usr/bin/python3.5 /usr/bin/python3


cd /tmp
rm -rf get-pip.py
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

pip3 install https://github.com/google/brotli/archive/master.zip
pip3 install https://github.com/jplana/python-etcd/archive/master.zip

pip3 install 'cython>=0.23.4' git+git://github.com/gevent/gevent.git#egg=gevent

pip3 install paramiko

pip3 install msgpack-python
pip3 install redis
pip3 install credis
pip3 install aioredis

pip3 install mongoengine

pip3 install bcrypt
pip3 install blosc
pip3 install certifi
pip3 install docker-py

pip3 install gitlab3
pip3 install gitpython
pip3 install html2text

# pip install pysqlite
pip3 install click
pip3 install influxdb
pip3 install ipdb
pip3 install ipython --upgrade
pip3 install jinja2
pip3 install netaddr

pip3 install reparted
pip3 install pytoml
pip3 install pystache
pip3 install pymongo
pip3 install psycopg2
pip3 install pathtools
pip3 install psutil

pip3 install pytz
pip3 install requests
pip3 install sqlalchemy
pip3 install urllib3
pip3 install zmq
pip3 install pyyaml
pip3 install websocket
pip3 install marisa-trie
pip3 install pylzma
pip3 install ujson
pip3 install watchdog
pip3 install colorlog