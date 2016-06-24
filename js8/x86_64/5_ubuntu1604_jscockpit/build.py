from JumpScale import j

j.do.createDir("/tmp/build")
vols='/bd_build:%s#/build:/tmp/build'%j.sal.fs.getcwd()
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1604_golang', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)

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

printInfo("create builder container")

container = d.cuisine

container.package.mdupdate()

container.apps.portal.install(start=False)
container.apps.mongodb.build(start=False)
container.apps.influxdb.build(start=False)
container.apps.grafana.build(start=False)
container.core.run("js 'j.actions.resetAll()'")  # FIXME find why if we don't reset action before installing controller, everything explode
container.apps.controller.build(start=False)
container.apps.caddy.build(start=False)
container.apps.cockpit.build(start=False)
container.package.install('shellinabox')
bin_path = container.bash.cmdGetPath('shellinaboxd')
container.core.file_copy(bin_path, "$binDir")

printInfo('clean before creating image')
container.core.dir_remove("$goDir/src/*")
container.core.dir_remove("$tmpDir/*")
container.core.dir_remove("$varDir/data/*")

d.commit("jumpscale/%s" % name, delete=True, force=True)




