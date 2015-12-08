#!/bin/bash
set -e
source /code/buildconfig
set -x



ORG_PATH="github.com/coreos"
REPO_PATH="${ORG_PATH}/etcd"

export GOPATH=/tmp/etcdgopath

if [ ! -d $GOPATH ]; then
    mkdir -p $GOPATH
fi


mkdir -p /build/etcd

go get -d -u github.com/coreos/etcd

cd $GOPATH/src/$REPO_PATH
git checkout v2.2.2

go get -d .

CGO_ENABLED=0 go build -a -installsuffix cgo -ldflags "-s -X ${REPO_PATH}/version.GitSHA=v2.2.2" -o /build/etcd/etcd .

cp /code/services/1_etcd/Dockerfile /build/etcd
