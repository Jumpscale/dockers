from JumpScale import j

name="ubuntu1604_python3"

j.do.createDir("/tmp/build")
vols='/bd_build:%s#/build:/tmp/build'%j.sal.fs.getcwd()
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1604', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)

j.actions.resetAll()
d.cuisine.installer.base()
d.cuisine.installerdevelop.python()
d.cuisine.installerdevelop.pip()
d.cuisine.installerdevelop.installJS8Deps()
d.cuisine.installerdevelop.cleanup()

d.commit("jumpscale/%s" % name, delete=True, force=True)

