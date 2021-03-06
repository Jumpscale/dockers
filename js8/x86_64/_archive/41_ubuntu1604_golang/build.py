from JumpScale import j

j.sal.fs.createDir("/tmp/build")
vols = '/bd_build:%s#/build:/tmp/build' % j.sal.fs.getcwd()
print(vols)

d = j.sal.docker.create(name='build',
                        ports='',
                        vols=vols,
                        volsro='',
                        stdout=True,
                        base='jumpscale/ubuntu1604_js8',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        cpu=None,
                        mem=0,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False)

name = "ubuntu1604_golang"

d.cuisine.development.golang.install()

d.commit("jumpscale/%s" % name, delete=True, force=True)
