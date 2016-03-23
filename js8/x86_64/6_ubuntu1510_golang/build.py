from JumpScale import j


j.do.createDir("/tmp/build/opt/jumpscale8")
vols='/bd_build:%s#/build:/tmp/build'%curdir
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510_js8', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)
# d=j.sal.docker.get('build')



GOLANG="""
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

apt-get update

$minimal_apt_get_install golang rsync

"""
def golang():
    d.cuisine.core.run_script(GOLANG)
j.actions.start(golang, runid='ubuntu1510_golang')
