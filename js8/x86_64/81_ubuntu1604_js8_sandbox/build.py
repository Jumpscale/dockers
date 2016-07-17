from JumpScale import j

name = 'ubuntu1604_sandbox'
logger = j.logger.get('j.docker.sandboxer')

j.actions.resetAll()


d = j.sal.docker.create(name='js8_sandbox',
                         stdout=True,
                         base='jumpscale/ubuntu1604',
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False,
                         vols="/out:/storage/builder/sandbox_ub1604")


logger.info("create sandbox")

d.executor.sshclient.rsync_up("/storage/builder/sandbox_ub1604/js8/jumpscale8/","/opt/jumpscale8/")

s="""
set -ex
cd /opt/jumpscale8
source env.sh
js 'j.tools.console.echo("SUCCEEDED")'
"""
d.cuisine.core.run_script(s)

s="""
find -regex '.*__pycache__.*' -delete
rm -rf /var/log
mkdir -p /var/log/apt
rm -rf /var/tmp
mkdir -p /var/tmp
"""
d.cuisine.core.run_script(s)


add='source /opt/jumpscale8/env.sh'
prof=d.cuisine.core.file_read("/root/.profile")

if not add in prof:
    prof+='\n%s\n'%add
    d.cuisine.core.file_write("/root/.profile",prof)


d.commit("jumpscale/%s" % name, delete=True, force=True)
