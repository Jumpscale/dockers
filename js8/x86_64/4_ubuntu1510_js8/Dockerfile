FROM jumpscale/ubuntu1510_python3

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

CMD ["/sbin/my_init"]
