#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

set +ex
apt-get clean
rm -rf /var/tmp/*
# rm -rf /var/lib/apt/lists/*
rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup
#rm -f /etc/ssh/ssh_host_*