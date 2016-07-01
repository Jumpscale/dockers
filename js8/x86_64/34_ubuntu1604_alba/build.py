from JumpScale import j

name = "ubuntu1604-alba"

d = j.sal.docker.create(name='build-' + name,
                             stdout=True,
                             base='jumpscale/ubuntu1604',
                             nameserver=['8.8.8.8'],
                             replace=True,
                             ssh=True,
                             myinit=True,
                             detach=True,
                             privileged=True)

d.cuisine.apps.alba.build(start=False)
# clean source file
# d.cuisine.core.dir_remove('$tmpDir')
# d.cuisine.core.dir_ensure('$tmpDir')

d.commit("jumpscale/%s" % name, delete=True, force=True)
