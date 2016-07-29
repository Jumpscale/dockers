
from JumpScale import j

def docker(reset=False):
    if reset:
        j.actions.resetAll()

    j.sal.btrfs.subvolumeCreate("/storage/builder")
    j.sal.btrfs.subvolumeCreate("/storage/builder/sandbox_ub1604")

    d = j.sal.docker.create(name='build',
                             stdout=True,
                             base="jumpscale/ubuntu1604",
                             nameserver=['8.8.8.8'],
                             replace=reset,
                             myinit=True,
                             ssh=True,
                             sharecode=False,
                             setrootrndpasswd=False,
                             vols="/out:/storage/builder/sandbox_ub1604")  

    return d

def base(push=True,reset=True):
    name="ubuntu1604_js"
    d.cuisine.installer.base()
    d.cuisine.installerdevelop.python()
    d.cuisine.installerdevelop.pip()
    d.cuisine.installerdevelop.installJS8Deps()

    d.cuisine.installerdevelop.cleanup()

    if reset:
        d.commit("jumpscale/ubuntu1604_js", delete=True, force=True,push=push)


def shellinabox():
    d.cuisine.package.install('shellinabox')
    bin_path = d.cuisine.bash.cmdGetPath('shellinaboxd')
    d.cuisine.core.file_copy(bin_path, "$binDir")

def cleanup():
    d.cuisine.core.dir_remove("$goDir/src/*",force=True)
    d.cuisine.core.dir_remove("$tmpDir/*",force=True)
    d.cuisine.core.dir_remove("$varDir/data/*",force=True)
    d.cuisine.installerdevelop.cleanup()
    C="""
    cd /opt;find . -name '*.pyc' -delete
    cd /opt;find . -name '*.log' -delete
    cd /opt;find . -name '__pycache__' -delete
    """
    d.cuisine.core.run_script(C)


#### ARGS
push=True
reset=False


#### MAIN

d=docker(reset=reset)

base(push=push,reset=reset)

d.cuisine.installerdevelop.jumpscale8()
if reset:
    cleanup()
    d.commit("jumpscale/ubuntu1604_js8", delete=True, force=True,push=True)

d.cuisine.golang.install()

if reset: #can only commit/push when we stared from clean slate
    cleanup()
    d.commit("jumpscale/ubuntu1604_golang", delete=True, force=True,push=True)

d.cuisine.apps.portal.install(start=False)
d.cuisine.apps.mongodb.build(start=False)

d.cuisine.apps.grafana.build(start=False)
d.cuisine.apps.controller.build(start=False)
d.cuisine.apps.caddy.build(start=False)
d.cuisine.apps.stor.build(start=False)
d.cuisine.apps.cockpit.build(start=False)

d.cuisine.apps.influxdb.install()  
#@todo influxdb does not install, also need to link back into bin
#also copy cofig file


d.cuisine.geodns.install()

d.cuisine.apps.fs.build(start=False)
cleanup()
#this is the full one, we can commit
d.commit("jumpscale/ubuntu1604_js_development", delete=True, force=True,push=True)



