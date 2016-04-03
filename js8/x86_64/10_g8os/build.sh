#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update

$minimal_apt_get_install libpython3.5-dev python3.5-dev
$minimal_apt_get_install wget

cd /tmp
rm -rf get-pip.py
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py

pip install --upgrade pip

pip install https://github.com/g8os/builder/archive/master.zip