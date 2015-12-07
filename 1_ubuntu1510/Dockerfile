FROM ubuntu:15.10

MAINTAINER JumpScale

ADD ../scripts /bd_build
ADD . /bd_build


ENV HOME /root/

RUN /bd_build/prepare.sh && \
	/bd_build/system_services.sh && \
	/bd_build/utilities.sh && \
	/bd_build/cleanup.sh


CMD ["/sbin/my_init"]
