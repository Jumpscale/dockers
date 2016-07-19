
from JumpScale import j

name = "ubuntu1604_development"

d = j.sal.docker.create(name='build',
                        stdout=True,
                        base='jumpscale/ubuntu1604_golang',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False)


j.actions.resetAll()


repos = [
    'https://github.com/Jumpscale/ays_jumpscale8.git',
    'https://github.com/Jumpscale/jumpscale_core8.git',
    'https://github.com/JumpScale/jscockpit.git'
]

for url in repos:
    d.cuisine.git.pullRepo(url, ssh=False)

d.cuisine.package.mdupdate()

d.cuisine.apps.portal.install(start=False)
d.cuisine.apps.mongodb.build(start=False)
d.cuisine.apps.influxdb.build(start=False)
d.cuisine.apps.grafana.build(start=False)
d.cuisine.apps.controller.build(start=False)
d.cuisine.apps.caddy.build(start=False)
d.cuisine.apps.stor.build(start=False)
d.cuisine.apps.cockpit.build(start=False)
d.cuisine.geodns.install()
d.cuisine.package.install('shellinabox')
bin_path = d.cuisine.bash.cmdGetPath('shellinaboxd')
d.cuisine.core.file_copy(bin_path, "$binDir")

d.cuisine.core.dir_remove("$goDir/src/*")
d.cuisine.core.dir_remove("$tmpDir/*")
d.cuisine.core.dir_remove("$varDir/data/*")

d.commit("jumpscale/%s" % name, delete=True, force=True)
