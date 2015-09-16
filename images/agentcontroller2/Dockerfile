FROM jumpscale/ubuntu:15.04
MAINTAINER JumpScale

#Install agentcontroller2
#NOTE: we force start everything before we do install, to make sure installation go smooth
RUN ays start && ays install -n agentcontroller2 --data "instance.param.webservice.host::8966 instance.param.redis.host:localhost:9999 instance.param.redis.password:"

#Install agent2
RUN ays start && ays install -n agent2 --data "instance.agentcontroller:http://127.0.0.1:8966/ instance.gid:1 instance.nid:1 instance.roles:''"

#Install agentcontroller2_client
#NOTE: no need to start everything, this is just an extension
RUN ays install -n agentcontroller2_client --data "instance.param.redis.address:localhost instance.param.redis.port:9999 instance.param.redis.password:"

CMD ["/sbin/my_init"]
