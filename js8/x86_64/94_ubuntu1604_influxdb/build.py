from JumpScale import j

name = "ubuntu1604_influxdb"
d = j.sal.docker.create(name=name,
                        ports='',
                        volsro='',
                        stdout=True,
                        base='jumpscale/ubuntu1604_js8',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        cpu=None,
                        mem=0,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False,
                        vols="")


j.actions.resetAll()

d.cuisine.apps.influxdb.install(reset=True, start=True)

d.cuisine.core.dir_remove("$tmpDir/*")

d.commit("jumpscale/%s" % name, delete=True, force=True)
