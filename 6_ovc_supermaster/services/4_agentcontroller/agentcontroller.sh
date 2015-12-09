#!/bin/bash
set -e
source /code/buildconfig
set -x

export GOPATH=/tmp/agentcontroller2gopath

#change this to build @todo (*1*), do agent too

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
godep restore
godep go install


mv -f $GOPATH/bin/agentcontroller2 /usr/bin/
cp -f /code/services/4_agentcontroller/agentcontroller.toml /etc/agentcontroller.toml

#mkdir /etc/service/agentcontroller
#cp /code/services/agentcontroller/agentcontroller.runit /etc/service/agentcontroller/run

if [ -d /build/agentcontroller ]; then
  rm -rf /build/agentcontroller
fi
mkdir /build/agentcontroller
#TODO: Commented out the next line since it fails
#cp /user/agent* /build/agentcontroller/
cp /code/services/4_agentcontroller/agentcontroller.toml /build/agentcontroller/
