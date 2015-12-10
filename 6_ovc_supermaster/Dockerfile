FROM jumpscale/ubuntu1510_golang

MAINTAINER JumpScale

COPY buildconfig /code/buildconfig

COPY services/1_etcd /code/services/1_etcd
RUN /code/services/1_etcd/etcd.sh

COPY services/2_redis /code/services/2_redis
RUN /code/services/2_redis/redis.sh

COPY services/3_skydns /code/services/3_skydns
RUN /code/services/3_skydns/skydns.sh

COPY services/4_agentcontroller /code/services/4_agentcontroller
RUN /code/services/4_agentcontroller/agentcontroller.sh

COPY services/5_vulcand /code/services/5_vulcand
RUN /code/services/5_vulcand/vulcand.sh

COPY services/6_pxeboot /code/services/6_pxeboot
RUN /code/services/6_pxeboot/pxeboot.sh

COPY cleanup.sh /code/cleanup.sh
RUN /code/cleanup.sh

VOLUME /opt/build
