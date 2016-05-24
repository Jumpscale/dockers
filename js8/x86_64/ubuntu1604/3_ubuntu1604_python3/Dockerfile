FROM jumpscale/ubuntu1604

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh && \
	bash /bd_build/clean.sh

CMD ["/sbin/my_init"]
