#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

$minimal_apt_get_install wget

apt-get update

rm -rf get-pip.py
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3.5 get-pip.py


pip install https://github.com/g8os/builder/archive/master.zip