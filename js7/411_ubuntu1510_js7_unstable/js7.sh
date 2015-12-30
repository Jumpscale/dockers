#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

export SANDBOX=0
export JSBRANCH=ays_unstable
export AYSBRANCH=ays_unstable
cd /tmp;rm -f install.sh;curl -k https://raw.githubusercontent.com/Jumpscale/jumpscale_core7/ays_unstable/install/install.sh > install.sh;bash install.sh

