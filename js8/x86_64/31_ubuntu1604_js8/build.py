from JumpScale import j

name = "ubuntu1604_js8"

j.do.createDir("/tmp/build")
vols = '/bd_build:%s#/build:/tmp/build' % j.sal.fs.getcwd()
print(vols)

d = j.sal.docker.create(name='build',
                        ports='',
                        vols=vols,
                        volsro='',
                        stdout=True,
                        base='jumpscale/ubuntu1604_python3',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        cpu=None,
                        mem=0,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False)

#should not be needed but does not work for now
j.actions.resetAll()

d.cuisine.installerdevelop.jumpscale8()

d.commit("jumpscale/%s" % name, delete=True, force=True)
