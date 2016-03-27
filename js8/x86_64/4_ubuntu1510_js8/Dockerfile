FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN /bd_build/build.sh


CMD ["/sbin/my_init"]
CMD ["js 'j.tools.cuisine.local.builder.all()'"]