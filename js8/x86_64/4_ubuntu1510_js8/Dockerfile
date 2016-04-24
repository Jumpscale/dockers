FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

ENV remotedockerip=`diip remote1`

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

CMD ["/sbin/my_init"]
