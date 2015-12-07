FROM jumpscale/ubuntu1510_python3

MAINTAINER JumpScale

#ADD ../scripts /bd_build
ADD . /bd_build


ENV HOME /root/

RUN /bd_build/js8.sh && \
    /bd_build/cleanup.sh

CMD ["/sbin/my_init"]
