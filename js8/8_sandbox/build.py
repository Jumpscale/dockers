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
git pull
cd /
'''



print ("SANDBOX")
SANDBOX='''
d=j.atyourservice.debug.get("main")
d.addSandboxSource("/usr/bin/rsync")
d.sandbox()
'''



COPY="""
j.do.delete("/build/opt/jumpscale8/")
j.do.delete("/build/optvar/")
j.do.copyTree("/opt/jumpscale8/","/build/opt/jumpscale8/")
j.do.copyTree("/optvar/","/build/optvar/")
j.do.delete("/build/opt/jumpscale8/bin/metadata.db")
"""

d.cuisine.run_script(PREPARE)
d.cuisine.execute_jumpscript(SANDBOX)
d.cuisine.execute_jumpscript(COPY)
