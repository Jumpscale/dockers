FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN /bd_build/build.sh


CMD ["/sbin/my_init"]

CMD ["git clone -b test_buildall https://github.com/0-complexity/g8_lab_internal.git"]
