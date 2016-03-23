from JumpScale import j


# j.do.createDir("/tmp/build")
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
def prepare():
    d.cuisine.core.run_script(PREPARE)
j.actions.start(prepare, runid='sandbox')


print ("SANDBOX")
SANDBOX='''
d=j.atyourservice.debug.get("main")
d.addSandboxSource("/usr/bin/rsync")
d.sandbox()
'''
def sandbox():
    d.cuisine.core.run_script(SANDBOX)
j.actions.start(sandbox, runid='sandbox')


COPY="""
j.do.delete("/build/opt/jumpscale8/")
j.do.delete("/build/optvar/")
j.do.copyTree("/opt/jumpscale8/","/build/opt/jumpscale8/")
j.do.copyTree("/optvar/","/build/optvar/")
j.do.delete("/build/opt/jumpscale8/bin/metadata.db")
"""
def copy():
    d.cuisine.core.run_script(copy)
j.actions.start(copy, runid='sandbox')
