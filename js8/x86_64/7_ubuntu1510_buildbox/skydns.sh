#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

ORG_PATH="github.com/skynetservices"
REPO_PATH="${ORG_PATH}/skydns"

$minimal_apt_get_install golang
export GOPATH=/tmp/skydnsdgopath

if [ ! -d $GOPATH ]; then
    mkdir -p $GOPATH
fi

mkdir -p /build/skydns

go get -d -u $REPO_PATH

cd $GOPATH/src/$REPO_PATH
# git checkout 2.5.3a

go get -d .

CGO_ENABLED=0 go build -a -installsuffix cgo -ldflags "-s" -o /opt/jumpscale8/bin/skydns .

rm -rf $GOPATH