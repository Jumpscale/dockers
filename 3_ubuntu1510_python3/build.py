from JumpScale import j


j.do.createDir("/tmp/build")
vols='/bd_build:%s#/build:/tmp/build'%j.sal.fs.getcwd()
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=True)
#d=j.sal.docker.get('build')

C='''
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x


apt-get update

$minimal_apt_get_install libpython3.5-dev python3.5-dev libffi-dev gcc build-essential autoconf libtool pkg-config libpq-dev 
$minimal_apt_get_install libsqlite3-dev 
#$minimal_apt_get_install net-tools sudo

cd /tmp
sudo rm -rf brotli/
git clone https://github.com/google/brotli.git
cd /tmp/brotli/
python setup.py install
cd tests
make
cd ..
cp /tmp/brotli/tools/bro /usr/local/bin/
rm -rf /tmp/brotli

#DANGEROUS TO RENAME PYTHON
#rm -f /usr/bin/python
#rm -f /usr/bin/python3
#ln -s /usr/bin/python3.5 /usr/bin/python
#ln -s /usr/bin/python3.5 /usr/bin/python3


cd /tmp
rm -rf get-pip.py
wget https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

cd /tmp
git clone https://github.com/jplana/python-etcd.git
cd python-etcd
python3.5 setup.py install


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
'''

d.cuisine.run_script(C)

CLEANUP='''
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get clean
rm -rf /bd_build
rm -rf /tmp/* /var/tmp/*
# rm -rf /var/lib/apt/lists/*
rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup

rm -f /etc/ssh/ssh_host_*

'''
d.cuisine.local.run_script(CLEANUP)

from IPython import embed
embed()


