FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flusall()'

RUN js 'j.tools.cuisine.local.builder.all()'


CMD ["/sbin/my_init"]