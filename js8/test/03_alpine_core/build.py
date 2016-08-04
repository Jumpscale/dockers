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
time.sleep(2)

template = """\
[main]
max_jobs = 200
message_ID_file = "/var/core.mid"
include = "$cfgDir/core/conf"

[controllers]
[controllers.main]
url = "http://172.17.0.1:8966"

[channel]
cmds = [] # empty for long polling from all defined controllers, or specif controllers keys

[extension.jumpscript]
binary = "python"
cwd = "./extensions/jumpscript"
args = ["wrapper.py", "{domain}", "{name}"]
    [extension.jumpscript.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../"

[extension.jumpscript_content]
binary = "python"
cwd = "./extensions/jumpscript"
args = ["wrapper_content.py"]
    [extension.jumpscript_content.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../"

[extension.js_daemon]
binary = "python"
cwd = "./extensions/jumpscript"
args = ["executor.py"]
    [extension.js_daemon.env]
    SOCKET = "/tmp/jumpscript.sock"
    PYTHONPATH = "../:/opt/jumpscale8/lib"
    JUMPSCRIPTS_HOME = "/opt/jumpscale8/apps/agent8/jumpscripts/"

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
home = d.cuisine.core.args_replace('$tmplsDir/cfg/core/')
config = d.cuisine.core.args_replace(template)

d.cuisine.core.file_write('$cfgDir/core/core.toml', config)

cmd = "$binDir/core -gid 1 -nid 1 -c $cfgDir/core/core.toml"

pm.ensure(name="controller", cmd=cmd, env={}, path=home)