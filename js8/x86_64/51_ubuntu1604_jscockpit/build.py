from JumpScale import j

j.do.createDir("/tmp/build")
vols='/bd_build:%s#/build:/tmp/build'%j.sal.fs.getcwd()
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1604_golang', \
    nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, ssh=True, sharecode=False)


name="g8cockpit"


def printInfo(msg):
    print (msg)

def update():
    """
    Update the git repo used during installation of the cockpit.
    Run that before doing install to be sure to have last code.
    """
    printInfo("Update required git repository to last version")
    repos = [
        'https://github.com/Jumpscale/ays_jumpscale8.git',
        'https://github.com/Jumpscale/jumpscale_core8.git',
        'https://github.com/JumpScale/jscockpit.git'
    ]
    for url in repos:
        j.do.pullGitRepo(url=url, executor=d.cuisine.executor,ssh=False)


update()

"""
Build g8cockpit docker image
"""

printInfo("create builder cuisine")

cuisine = d.cuisine

cuisine.package.mdupdate()

cuisine.apps.portal.install(start=False)
cuisine.apps.mongodb.build(start=False)
cuisine.apps.influxdb.build(start=False)
cuisine.apps.grafana.build(start=False)
cuisine.core.run("js 'j.actions.resetAll()'")  # FIXME find why if we don't reset action before installing controller, everything explode
cuisine.apps.controller.build(start=False)
cuisine.apps.caddy.build(start=False)
cuisine.apps.cockpit.build(start=False)
cuisine.package.install('shellinabox')
bin_path = cuisine.bash.cmdGetPath('shellinaboxd')
cuisine.core.file_copy(bin_path, "$binDir")

printInfo('clean before creating image')
cuisine.core.dir_remove("$goDir/src/*")
cuisine.core.dir_remove("$tmpDir/*")
cuisine.core.dir_remove("$varDir/data/*")

d.commit("jumpscale/%s" % name, delete=True, force=True)




