FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/redis.sh && \
	/bd_build/etcd.sh && \
	/bd_build/skydns.sh && \
	/bd_build/vulcand.sh && \
	/bd_build/agentcontroller.sh

CMD ["/sbin/my_init"]
CMD ["js 'j.tools.cuisine.local.builder.all()'"]