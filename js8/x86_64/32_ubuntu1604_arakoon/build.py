from JumpScale import j

name = "ubuntu1604_arakoon"

d = j.sal.docker.create(name='build_' + name, stdout=True, base='jumpscale/ubuntu1604_js8',
                        nameserver=['8.8.8.8'], replace=True, cpu=None, mem=0, jumpscale=False,
                        ssh=True, myinit=True, sharecode=False)
# build arakoon
d.cuisine.apps.arakoon.build(start=False)
# clean source file
d.cuisine.core.dir_remove('$tmpDir')
d.cuisine.core.dir_ensure('$tmpDir')


d.commit("jumpscale/%s" % name, delete=True, force=True)
