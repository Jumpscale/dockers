from JumpScale import j

name = "ubuntu1604_jsagent"
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

repos = ['https://github.com/Jumpscale/jumpscale_core8.git']
for url in repos:
    d.cuisine.development.git.pullRepo(url, ssh=False)

d.cuisine.package.mdupdate()
d.cuisine.package.install('nmap')
d.cuisine.development.pip.install('uvloop')

d.cuisine.apps.jsagent.install(reset=True, start=False)

d.cuisine.core.dir_remove("$TMPDIR/*")
d.cuisine.core.dir_remove("$VARDIR/data/*")

d.commit("jumpscale/%s" % name, delete=True, force=True)
