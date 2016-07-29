from JumpScale import j

name = 'ubuntu1604_sandbox'
logger = j.logger.get('j.docker.sandboxer')

# base='jumpscale/ubuntu1604_volumedriver'
base='jumpscale/ubuntu1604_js8_development'

j.actions.resetAll()

j.sal.btrfs.subvolumeCreate("/storage/builder")
j.sal.btrfs.subvolumeCreate("/storage/builder/sandbox_ub1604")

d1 = j.sal.docker.create(name='build',
                         stdout=True,
                         base=base,
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False,
                         vols="/out:/storage/builder/sandbox_ub1604")


# d2 = j.sal.docker.create(name='build_alpine',
#                          stdout=True,
#                          base='jumpscale/alpine',
#                          nameserver=['8.8.8.8'],
#                          replace=True,
#                          myinit=False,
#                          ssh=True,
#                          sharecode=False,
#                          setrootrndpasswd=False)


# Sandbox need to happens in two step
# first we copy all required libs and binaries under /opt/jumpscale8
# second we dedupe all the files and generated the flist.
# These two steps needs to happens in two script, doing it all in one script segfault.

repos = [
    'https://github.com/Jumpscale/ays_jumpscale8.git',
    'https://github.com/Jumpscale/jumpscale_core8.git',
    'https://github.com/JumpScale/jscockpit.git'
]

for url in repos:
    d1.cuisine.git.pullRepo(url, ssh=False)

d1.cuisine.package.mdupdate()

d1.cuisine.sandbox.do("/out")

# logger.info("commit image jumpscale/%s" % name)
# d1.commit("jumpscale/%s" % name, delete=True, force=True)
