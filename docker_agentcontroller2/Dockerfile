FROM jumpscale/ubuntu1504

MAINTAINER JumpScale

EXPOSE 8966 9999 18384

#deployed in docker as example
#ssh keys are in mem

rm -rf /opt/jumpscale7/hrd/apps/jumpscale__redis__main/

RUN ays install -n nodessh -i ovh4 ... the data parts ...
RUN ays install -n nodessh -i ovh5 ... the data parts ...

RUN ays install -n redis --data 'instance.param.disk:0 instance.param.mem:100 instance.param.passwd: instance.param.port:9999 instance.param.unixsocket:0'

RUN ays install -n nginx -i main

#Install redis by default
RUN ays install -n agentcontroller2 --data param.webservice.host=':8966'#param.redis.host='localhost:9999'#param.redis.password=''   

RUN ays install -n go --data gopath='/opt/go_workspace'   

#make sure we have the latest version
RUN ays build -n agentcontroller2

#install influxdb
...

#generate an ssl key for nginx / which is front of agentcontroller2
#deploy rightkeys & config on nginx
#restart nginx
RUN ays install -n agentcontroller2_keys --consume ac/agentcontroller!main,ws/ngnix!main

RUN ays install -n agentcontroller2_client --consume ac/agentcontroller!main
#agent2 for local usage
RUN ays install -n agent2 --consume ac/agentcontroller!main

#generate client certificate for ovh4, deploy over ssh the agentcontroller client using keys as generated above
RUN ays install -n agent2  -i ovh4agent --consume ac/agentcontroller!main,node/nodessh!ovh4
RUN ays install -n agent2  -i ovh5agent --consume ac/agentcontroller!main,node/nodessh!ovh5

#configure agents to use redis
#use the agent to deploy over ays redis on each node (will need new ays which does not autostart with tmux)
#use the agents to start redis underneath agent
#deploy example jumpscript which gets scheduled every 10 sec to gather stats & send to redis (see the perftesttools in ext jumpscale/lib)
#deploy lua script (to be created) which gets aggregated stats from redis queue & sends to stdout so can be picked up by agent to be send to agentcontroller
#do this for all agents known to agentcontroller
#is new ays recipe
RUN ays install -n agentcontroller2_statsplugin --consume ac/agentcontroller!main


CMD ["/sbin/my_init"]


