FROM ubuntu:15.04
MAINTAINER JumpScale

ADD . /bd_build

RUN /bd_build/prepare.sh && \
	/bd_build/system_services.sh && \
	/bd_build/utilities.sh && \
	/bd_build/cleanup.sh

#Enable SSHD
RUN rm /etc/service/sshd/down

#Pregenerate the host SSH keys
RUN dpkg-reconfigure openssh-server

#Set default login password
RUN echo root:gig1234 | chpasswd

RUN apt-get update
RUN apt-get install -y mc git python2.7 wget curl tmux
RUN apt-get upgrade

#Install jumpscale
RUN export JSBRANCH = ays_unstable
RUN export AYSBRANCH = ays_unstable
RUN cd /tmp && rm -f install.sh && curl -k https://raw.githubusercontent.com/Jumpscale/jumpscale_core7/master/install/install.sh > install.sh && bash install.sh
RUN cd /opt/code/github/jumpscale/jumpscale_core7;git remote set-url origin git@github.com:Jumpscale/jumpscale_core7.git
RUN cd /opt/code/github/jumpscale/ays_jumpscale7;git remote set-url origin git@github.com:Jumpscale/ays_jumpscale7.git
#Install runit ays service
ADD runit/ays /etc/service/ays

#Install redis by default
RUN ays install -n redis --data 'instance.param.disk:0 instance.param.mem:100 instance.param.passwd: instance.param.port:9999 instance.param.unixsocket:0'
CMD ["/sbin/my_init"]
