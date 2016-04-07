FROM ubuntu:15.10

MAINTAINER JumpScale

ADD . /bd_build


ENV HOME /root/

RUN bash /bd_build/build.sh

RUN js 'j.core.db.flushall()'

RUN js 'j.tools.cuisine.local.installerdevelop.pip()'
RUN js 'j.tools.cuisine.local.installerdevelop.python()'
RUN js 'j.tools.cuisine.local.portal.install(start=True)'
RUN js 'j.tools.cuisine.local.core.build(start=True)'
RUN js 'j.tools.cuisine.local.syncthing.build(start=True)'
RUN js 'j.tools.cuisine.local.controller.build(start=True)'
RUN js 'j.tools.cuisine.local.fs.build(start=True)'
RUN js 'j.tools.cuisine.local.stor.build(start=True)'
RUN js 'j.tools.cuisine.local.etcd.build(start=True)'
RUN js 'j.tools.cuisine.local.mongodb.build(start=True)'
RUN js 'j.tools.cuisine.local.caddy.build(start=True)'
RUN js 'j.tools.cuisine.local.influxdb.build(start=True)'
RUN js 'j.tools.cuisine.local.weave.build(start=True)'
RUN js 'j.tools.cuisine.local.redis.build(start=True)'


CMD ["/sbin/my_init"]