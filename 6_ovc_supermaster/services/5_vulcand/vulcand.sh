set -e
source /code/buildconfig
set -x


export GOPATH=/tmp/vulcandgopath

if [ ! -d $GOPATH]; then
    mkdir -p $GOPATH
fi

go get github.com/vulcand/vulcand

mkdir -p /build/vulcand
cp $GOPATH/bin/vulcand /build/vulcand/


#mkdir /etc/service/skydns
#cp /code/services/skydns/skydns.runit /etc/service/skydns/run
