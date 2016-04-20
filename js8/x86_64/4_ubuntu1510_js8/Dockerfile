FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

ENV TERM="xterm-256color"

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

RUN js 'j.tools.cuisine.local.builder.all(start=False, sandbox=True, stor_addr="https://stor.jumpscale.org/storx/")'



CMD ["/sbin/my_init"]
