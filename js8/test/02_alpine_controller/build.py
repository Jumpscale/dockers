from JumpScale import j

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
                        sharecode=False,
                        setrootrndpasswd=False,
                        privileged=True)


d.cuisine.core.dir_ensure('/opt/')
pm = d.cuisine.processmanager.get(pm="tmux")

#mount the filessystem
cmd = "/usr/local/bin/fs -c /etc/fs/config.toml"
pm.ensure(name="aydofs", cmd=cmd, env={}, path='/', descr='')
