#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update

$minimal_apt_get_install git make

git config --global http.sslVerify false
git clone https://github.com/g8os/builder.git -v