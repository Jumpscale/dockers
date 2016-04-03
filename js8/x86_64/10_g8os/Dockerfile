FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

RUN sudo make build --makefile builder/Makefile

CMD ["/sbin/my_init"]