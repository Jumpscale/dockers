from JumpScale import j


vols='/bd_build:%s#/build:/tmp/build'%curdir
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510_buildbox', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)
# d=j.sal.docker.get('build')

print ("PREPARE")
PREPARE='''
set -ex
cd /opt/code/github/jumpscale/jumpscale_core8
git checkout .
echo 1
git pull
echo 2
cd /
echo 3
'''



print ("SANDBOX")
SANDBOX='''
d=j.atyourservice.debug.get("main")
d.addSandboxSource("/usr/bin/rsync")
d.sandbox()
'''



COPY="""
j.sal.fs.removeDirTree("/build/opt/jumpscale8/")
j.sal.fs.removeDirTree("/build/optvar/")
j.sal.fs.copyDirTree("/opt/jumpscale8/","/build/opt/jumpscale8/")
j.sal.fs.copyDirTree("/optvar/","/build/optvar/")
j.sal.fs.remove("/build/opt/jumpscale8/bin/metadata.db")
"""

d.cuisine.core.execute_bash(PREPARE)
d.cuisine.execute_jumpscript(SANDBOX)
d.cuisine.execute_jumpscript(COPY)
