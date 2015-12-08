#!/bin/bash
set -e

# create gopath
mkdir -p /gopath

export GOPATH=/gopath
echo 'export GOPATH=/gopath' >> /root/.bashrc

export PATH=$PATH:$GOPATH/bin
echo 'export PATH=$PATH:$GOPATH/bin' >> /root/.bashrc

# install godep
go get -u github.com/tools/godep
