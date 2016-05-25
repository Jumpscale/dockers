#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

export GOPATH=/tmp/agentcontroller2gopath


if [ -d $GOPATH/src/github.com/Jumpscale/agentcontroller2 ]; then
  cd $GOPATH/src/github.com/Jumpscale/agentcontroller2 && git pull
else
  if [ ! -d $GOPATH/src/github.com/Jumpscale ]; then
    mkdir -p $GOPATH/src/github.com/Jumpscale
  fi
  cd $GOPATH/src/github.com/Jumpscale && git clone https://github.com/Jumpscale/agentcontroller2.git
fi
cd $GOPATH/src/github.com/Jumpscale/agentcontroller2

go get -u github.com/tools/godep
export PATH=$PATH:$GOPATH/bin

godep restore
godep go install

mv -f $GOPATH/bin/agentcontroller2 /opt/jumpscale8/bin/

mkdir -p /optvar/cfg/
cp /bd_build/agentcontroller.toml /optvar/cfg/

rm -rf $GOPATH
