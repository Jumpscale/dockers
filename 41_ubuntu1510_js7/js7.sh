#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

export SANDBOX=0
cd /tmp;rm -f install.sh;curl -k https://raw.githubusercontent.com/Jumpscale/jumpscale_core7/master/install/install.sh > install.sh;bash install.sh

