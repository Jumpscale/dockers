FROM jumpscale/ubuntu1510_js8

MAINTAINER JumpScale

ENV HOME /root/

RUN js 'j.core.db.flushall()'

RUN js 'j.tools.cuisine.local.builder.all(start=True)'

CMD ["/sbin/my_init"]
