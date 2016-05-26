FROM jumpscale/ubuntu1604_js8

MAINTAINER JumpScale

ENV HOME /root/

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

RUN js 'j.tools.cuisine.local.builder.all(start=True)'

CMD ["/sbin/my_init"]
