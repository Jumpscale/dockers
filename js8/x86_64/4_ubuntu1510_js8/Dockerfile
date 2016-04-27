FROM jumpscale/ubuntu1510_python3

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

RUN js 'j.tools.cuisine.local.builder.all(start=True)'

CMD ["/sbin/my_init"]
