from JumpScale import j


# j.do.createDir("/tmp/build")
vols='/bd_build:%s#/build:/tmp/build'%curdir
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510_golang', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)
#d=j.sal.docker.get('build')

print ("BUILD ETCD")
C_ETCD='''
set -ex

ORG_PATH="github.com/coreos"
REPO_PATH="${ORG_PATH}/etcd"

export GOPATH=/tmp/etcdgopath

if [ ! -d $GOPATH ]; then
    mkdir -p $GOPATH
fi

# rm -rf /build/opt/etcd
# mkdir -p /build/opt/etcd

go get -d -u github.com/coreos/etcd

cd $GOPATH/src/$REPO_PATH
# git checkout v2.2.2

go get -d .

CGO_ENABLED=0 go build -a -installsuffix cgo -ldflags "-s -X ${REPO_PATH}/version.GitSHA=v2.2.2" -o /opt/jumpscale8/bin/etcd .

rm -rf $GOPATH

'''




C_redis='''
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

# groupadd -r redis && useradd -r -g redis redis

# $minimal_apt_get_install build-essential

mkdir -p /opt/redis
cd /opt/redis
wget http://download.redis.io/releases/redis-3.0.6.tar.gz
tar xzf redis-3.0.6.tar.gz
cd redis-3.0.6
make

# rm -rf /build/opt/redis
# mkdir -p /build/opt/redis
# rm -rf /build/optvar/redis/
# mkdir -p /build/optvar/redis/

rm -f /usr/local/bin/redis-server
rm -f /usr/local/bin/redis-cli
cp /opt/redis/redis-3.0.6/src/redis-server /opt/jumpscale8/bin/
cp /opt/redis/redis-3.0.6/src/redis-cli /opt/jumpscale8/bin/

mkdir -p /optvar/cfg/
cp /bd_build/redis.conf /optvar/cfg/

rm -rf /opt/redis

'''



C_skydns='''
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

ORG_PATH="github.com/skynetservices"
REPO_PATH="${ORG_PATH}/skydns"

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

'''


C_vulcand='''
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

'''

C_agentcontroller='''
#!/bin/bash
set -e
source /bd_build/buildconfig
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
export PATH=$PATH:$GOPATH/bin

godep restore
godep go install

mv -f $GOPATH/bin/agentcontroller2 /opt/jumpscale8/bin/

mkdir -p /optvar/cfg/
cp /bd_build/agentcontroller.toml /optvar/cfg/

rm -rf $GOPATH

'''

# d.cuisine.run_script(C_ETCD)
# d.cuisine.run_script(C_redis)
# d.cuisine.run_script(C_skydns)
# d.cuisine.run_script(C_vulcand)
d.cuisine.run_script(C_agentcontroller)
