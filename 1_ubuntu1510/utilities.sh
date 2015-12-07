#!/bin/bash
set -e
source /bd_build/buildconfig
set -x


$minimal_apt_get_install curl less mc python3.5 iproute2 iputils-arping inetutils-telnet inetutils-ftp rsync inetutils-traceroute iputils-ping iputils-tracepath iputils-clockdiff

$minimal_apt_get_install net-tools sudo

$minimal_apt_get_install mc git wget tmux

#rm -rf /usr/bin/python
#ln /usr/bin/python3.5 /usr/bin/python

## This tool runs a command as another user and sets $HOME.
cp /bd_build/bin/setuser /sbin/setuser

#Enable SSHD
rm /etc/service/sshd/down

#Pregenerate the host SSH keys
dpkg-reconfigure openssh-server

#Set default login password
echo root:gig1234 | chpasswd

sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

cd /tmp
rm -rf get-pip.py
wget https://bootstrap.pypa.io/get-pip.py

apt-get update

$minimal_apt_get_install libpython-dev python-dev libffi-dev gcc build-essential autoconf libtool pkg-config libpq-dev 
$minimal_apt_get_install libsqlite3-dev 

python get-pip.py

cd /tmp
git clone https://github.com/jplana/python-etcd.git
cd python-etcd
python3.5 setup.py install


pip install 'cython>=0.23.4' git+git://github.com/gevent/gevent.git#egg=gevent

pip install paramiko

pip install msgpack-python
pip install redis
pip install credis

pip install mongoengine

pip install bcrypt
pip install blosc
pip install certifi
pip install docker-py

pip install gitlab3
pip install gitpython
pip install html2text

pip install pysqlite
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

