FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

RUN cd builder
RUN sudo make build

CMD ["/sbin/my_init"]