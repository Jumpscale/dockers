from JumpScale import j
import time

name = "alpine_core"
j.actions.resetAll()

logger = j.logger.get('j.docker.alpine_core')

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
cmd = '/usr/local/bin/fs -c /etc/fs/config.toml'
pm.ensure(name="aydofs", cmd=cmd, env={}, path='/', descr='')

# we should wait for a second or two until the mount is complete
time.sleep(3)

template = """\
[main]
max_jobs = 200
message_ID_file = "/var/core.mid"
include = "$JSCFGDIR/core/conf"

[controllers]
[controllers.main]
url = "http://alpine_controller:8966"

[channel]
cmds = [] # empty for long polling from all defined controllers, or specif controllers keys

[extension.jumpscript]
binary = "$BINDIR/python3"
cwd = "./extensions/jumpscript"
args = ["wrapper.py", "{domain}", "{name}"]
    [extension.jumpscript.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../:$BASEDIR/lib:$BASEDIR/lib/lib-dynload/:$BASEDIR/bin:$BASEDIR/lib/python.zip:$BASEDIR/lib/plat-x86_64-linux-gn"

[extension.jumpscript_content]
binary = "$BINDIR/python3"
cwd = "./extensions/jumpscript"
args = ["wrapper_content.py"]
    [extension.jumpscript_content.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../:$BASEDIR/lib:$BASEDIR/lib/lib-dynload/:$BASEDIR/bin:$BASEDIR/lib/python.zip:$BASEDIR/lib/plat-x86_64-linux-gn"

[extension.js_daemon]
binary = "$BINDIR/python3"
cwd = "./extensions/jumpscript"
args = ["executor.py"]
    [extension.js_daemon.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../:$BASEDIR/lib:$BASEDIR/lib/lib-dynload/:$BASEDIR/bin:$BASEDIR/lib/python.zip:$BASEDIR/lib/plat-x86_64-linux-gn"
    JUMPSCRIPTS_HOME = "$BASEDIR/apps/agent8/jumpscripts/"

[extension.bash]
binary = "bash"
args = ['-c', 'T=`mktemp` && cat > $T && bash $T; EXIT=$?; rm -rf $T; exit $EXIT']

[logging]
    [logging.console]
    type = "console"
    levels = [2, 4, 7, 8, 9]

[hubble]
controllers = []
"""
# copy controller template config
home = d.cuisine.core.args_replace('$TEMPLATEDIR/cfg/core/')
config = d.cuisine.core.args_replace(template)

d.cuisine.core.file_write('$JSCFGDIR/core/core.toml', config)
d.cuisine.core.dir_ensure('$JSCFGDIR/core/conf')
d.cuisine.core.file_copy('$TEMPLATEDIR/cfg/core/conf/{basic.jumpscripts.toml,basic.syncthing.toml}', '$JSCFGDIR/core/conf')
cmd = "$BINDIR/core -gid 1 -nid 1 -c $JSCFGDIR/core/core.toml"

pm.ensure(name="controller", cmd=cmd, env={}, path=home)