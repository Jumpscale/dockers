#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

$minimal_apt_get_install wget

rm -rf get-pip.py
wget https://bootstrap.pypa.io/get-pip.py

apt-get update

python get-pip.py

pip install https://github.com/g8os/builder/archive/master.zip