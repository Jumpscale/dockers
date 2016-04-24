FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

ENV remotedockerip=`diip remote1`

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

RUN js 'exc = j.tools.executor.getSSHBased(\"$remotedockerip\", passwd="gig1234"); cuisine = j.tools.cuisine.get(exc); cuisine.builder.all(start=False, sandbox=True, stor_addr="https://stor.jumpscale.org/storx/")'



CMD ["/sbin/my_init"]
