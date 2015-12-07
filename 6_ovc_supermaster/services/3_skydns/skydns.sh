set -e
source /code/buildconfig
set -x

curl -L https://git.aydo.com/binary/skydns/raw/master/skydns -o /usr/bin/skydns
chmod a+x /usr/bin/skydns

mkdir -p /build/skydns
cp /usr/bin/skydns /build/skydns/

#mkdir /etc/service/skydns
#cp /code/services/skydns/skydns.runit /etc/service/skydns/run
