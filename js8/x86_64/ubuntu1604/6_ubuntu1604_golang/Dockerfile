FROM jumpscale/ubuntu1604_js8

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh


CMD ["/sbin/my_init"]
