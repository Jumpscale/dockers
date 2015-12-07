FROM jumpscale/ubuntu1510

MAINTAINER JumpScale

ADD . /bd_build

ENV HOME /root/

RUN /bd_build/python.sh

CMD ["/sbin/my_init"]
