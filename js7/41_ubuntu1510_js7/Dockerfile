FROM jumpscale/ubuntu1510_python2

MAINTAINER JumpScale

#ADD ../scripts /bd_build
ADD . /bd_build


ENV HOME /root/

RUN /bd_build/js7.sh && \
    /bd_build/cleanup.sh

CMD ["/sbin/my_init"]
