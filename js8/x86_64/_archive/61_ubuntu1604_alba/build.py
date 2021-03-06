from JumpScale import j

name = "ubuntu1604_alba"

j.actions.resetAll()

d = j.sal.docker.create(name='build',
                             stdout=True,
                             base='jumpscale/ubuntu1604_g8cockpit',
                             nameserver=['8.8.8.8'],
                             replace=True,
                             ssh=True,
                             myinit=True,
                             detach=True,
                             privileged=True,setrootrndpasswd=False)

d.cuisine.apps.alba.build(start=False)
# clean source file
d.cuisine.core.dir_remove('$TMPDIR')
d.cuisine.core.dir_ensure('$TMPDIR')

d.commit("jumpscale/%s" % name, delete=True, force=True)
