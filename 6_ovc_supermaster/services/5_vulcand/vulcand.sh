set -e
source /code/buildconfig
set -x


export GOPATH=/tmp/vulcandgopath

if [ ! -d $GOPATH]; then
    mkdir -p $GOPATH
fi

go get -d github.com/vulcand/vulcand

cd $GOPATH/src/github.com/vulcand/vulcand
CGO_ENABLED=0 go build -a -installsuffix nocgo .

mkdir -p /build/vulcand
cp $GOPATH/bin/vulcand /build/vulcand/
cp /code/services/5_vulcand/Dockerfile /build/vulcand
