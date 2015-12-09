#!/usr/bin/env bash

set -e
set -x


docker build -t ovc_supermaster .

if [ -d build ]; then
    rm -rf build
fi
mkdir -p build

docker run -v $PWD/build:/opt/build --rm ovc_supermaster /bin/sh -c "cp -R /build/* /opt/build/"
