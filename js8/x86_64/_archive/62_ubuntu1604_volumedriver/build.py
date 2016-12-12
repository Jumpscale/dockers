from JumpScale import j

name = "ubuntu1604_volumedriver"

j.actions.resetAll()

d = j.sal.docker.create(name='build',
                             stdout=True,
                             base='jumpscale/ubuntu1604_alba',
                             nameserver=['8.8.8.8'],
                             replace=True,
                             ssh=True,
                             myinit=True,
                             detach=True,
                             privileged=True,setrootrndpasswd=False)

d.cuisine.apps.volumedriver.build(start=False)

# clean source file
d.cuisine.core.dir_remove('$TMPDIR')
d.cuisine.core.dir_ensure('$TMPDIR')
d.cuisine.core.dir_remove('$CODEDIR/github/openvstorage')
d.cuisine.core.dir_remove('$CODEDIR/github/domsj')

d.commit("jumpscale/%s" % name, delete=True, force=True)
