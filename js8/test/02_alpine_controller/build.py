from JumpScale import j
import time

name = "alpine_controller"
j.actions.resetAll()

logger = j.logger.get('j.docker.alpine_controller')

d = j.sal.docker.create(name=name,
                        stdout=True,
                        base='jumpscale/alpine_aydofs',
                        nameserver=['8.8.8.8'],
                        myinit=False,
                        replace=True,
                        ssh=True,
                        ports="6379:9999 8966:8966",
                        sharecode=False,
                        setrootrndpasswd=False,
                        privileged=True)


d.cuisine.core.dir_ensure('/opt/')
pm = d.cuisine.processmanager.get(pm="tmux")

#mount the filessystem
cmd = '/usr/local/bin/fs -c /etc/fs/config.toml'
pm.ensure(name="aydofs", cmd=cmd, env={}, path='/', descr='')

# we should wait for a second or two until the mount is complete
time.sleep(2)

# start redis
cmd = '$binDir/redis-server'
pm.ensure(name='redis', cmd=cmd, env={}, path='/', descr='')

# copy controller template config
home = d.cuisine.core.args_replace('$tmplsDir/cfg/controller/')
template = d.cuisine.core.file_read(j.sal.fs.joinPaths(home, 'agentcontroller.toml'))
config = d.cuisine.core.args_replace(template)

dest = d.cuisine.core.args_replace('$cfgDir/controller/')
d.cuisine.core.dir_ensure(dest)
cfg_path = j.sal.fs.joinPaths(dest, 'agentcontroller.toml')
d.cuisine.core.file_write(cfg_path, config)

cmd = "/opt/jumpscale8/bin/controller -c %s" % cfg_path

pm.ensure(name="controller", cmd=cmd, env={}, path=home)