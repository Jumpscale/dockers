#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

export GOPATH=/tmp/vulcandgopath

if [ ! -d $GOPATH ]; then
    mkdir -p $GOPATH
fi

go get -d github.com/vulcand/vulcand

cd $GOPATH/src/github.com/vulcand/vulcand
CGO_ENABLED=0 go build -a -ldflags '-s' -installsuffix nocgo .
GOOS=linux go build -a -tags netgo -installsuffix cgo -ldflags '-w' -o ./vulcand .
GOOS=linux go build -a -tags netgo -installsuffix cgo -ldflags '-w' -o ./vctl/vctl ./vctl
GOOS=linux go build -a -tags netgo -installsuffix cgo -ldflags '-w' -o ./vbundle/vbundle ./vbundle

mkdir -p /build/vulcand
cp $GOPATH/src/github.com/vulcand/vulcand/vulcand /opt/jumpscale8/bin/
cp $GOPATH/src/github.com/vulcand/vulcand/vctl/vctl /opt/jumpscale8/bin/
cp $GOPATH/src/github.com/vulcand/vulcand/vbundle/vbundle /opt/jumpscale8/bin/

rm -rf $GOPATH
