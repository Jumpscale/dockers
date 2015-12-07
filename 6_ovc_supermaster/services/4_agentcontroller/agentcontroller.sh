#!/bin/bash
set -e
source /code/buildconfig
set -x

#change this to build @todo (*1*), do agent too
cd /tmp
curl -L https://git.aydo.com/binary/agentcontroller2/repository/archive.tar.gz -o agentcontroller2.tar.gz
tar xzvf agentcontroller2.tar.gz
cd agentcontroller2.git
mv agentcontroller2 /usr/bin/
rm /etc/agentcontroller2.toml
cd ..
rm -rf agentcontroller2.git
rm -f agentcontroller2.tar.gz
cp /code/services/4_agentcontroller/agentcontroller.toml /etc/agentcontroller.toml

#mkdir /etc/service/agentcontroller
#cp /code/services/agentcontroller/agentcontroller.runit /etc/service/agentcontroller/run

mkdir /build/agentcontroller
cp /user/agent* /build/agentcontroller/
cp /code/services/4_agentcontroller/agentcontroller.toml /build/agentcontroller/


