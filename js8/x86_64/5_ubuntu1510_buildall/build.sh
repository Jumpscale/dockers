#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update
$minimal_apt_get_install curl

/usr/bin/runsvdir -P /etc/service&