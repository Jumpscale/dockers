#!/bin/bash

ays install -n node.ssh -i ovh4 --data "instance.ip:94.23.38.89 instance.ssh.port:22 instance.login:root instance.password:'' instance.sshkey:ovh.rsa instance.jumpscale:False instance.branch:ays_instable"
# RUN ays install -n nodessh -i ovh5 ... the data parts ...

#Install redis by default
ays install -n redis --data 'instance.param.disk:0 instance.param.mem:100 instance.param.passwd: instance.param.port:9999 instance.param.unixsocket:0'

#Install nginx basic
ays install -n nginx -i main

ays install -n agentcontroller2 --data param.webservice.host='localhost:8966'#param.redis.host='localhost:9999'#param.redis.password=''
# install agentcontroller2_client
ays install -n agentcontroller2_client --data "instance.param.redis.address:localhost instance.param.redis.port:9999 param.redis.password:''"

# ays install -n go --data gopath='/opt/go_workspace'   

#make sure we have the latest version
# ays build -n agentcontroller2

#install influxdb
ays install -n influxdb

#generate an ssl key for nginx / which is front of agentcontroller2
#deploy rightkeys & config on nginx
#restart nginx
ays install -n agentcontroller2_keys --data "instance.country:AE instance.state:Dubai instance.locality:Dubai instance.organisation:GIG instance.commonname:localhost" \
--consume 'ac/agentcontroller2!main,ws/nginx!main'

# #generate client certificate for ovh4
ays install -n agent2_keys -i ovh4 --consume 'auth/agentcontroller2_keys!main'


# deploy over ssh the agent2 + client certificate
# !!! make sure to use the same host in instance.agentcontroller as the common name given in the server certificate creation !!!!!
ays install -n agent2  -i ovh4 --consume 'auth/agent2_keys!ovh4' --data 'instance.agentcontroller:https://localhost/controller/ instance.gid:1 instance.nid:1 instance.roles:agent'


#configure agents to use redis internally
ays install -n agent2_stats -i ovh4 --consume 'agent/agent2!ovh4'

#use the agent to deploy over ays redis on each node (will need new ays which does not autostart with tmux)
#use the agents to start redis underneath agent
#deploy example jumpscript which gets scheduled every 10 sec to gather stats & send to redis (see the perftesttools in ext jumpscale/lib)
#deploy lua script (to be created) which gets aggregated stats from redis queue & sends to stdout so can be picked up by agent to be send to agentcontroller
#do this for all agents known to agentcontroller
#is new ays recipe
# ays install -n agentcontroller2_statsplugin --consume ac/agentcontroller!main