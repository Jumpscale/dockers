#!/bin/bash
set -e
source /code/buildconfig
set -x

apt-get clean
rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup

rm -f /etc/ssh/ssh_host_*
