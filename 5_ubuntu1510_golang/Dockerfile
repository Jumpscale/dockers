FROM jumpscale/ubuntu1510_js8

MAINTAINER JumpScale

ADD ../scripts /bd_build
ADD . /bd_build


ENV HOME /root/

RUN /bd_build/golang.sh && /bd_build/cleanup.sh

CMD ["/sbin/my_init"]
