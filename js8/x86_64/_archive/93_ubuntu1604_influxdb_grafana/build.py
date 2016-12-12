from JumpScale import j

# d = j.sal.docker.get(name='build')
d = j.sal.docker.create(name='build',
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
                        vols="/out:/storage/builder/sandbox_ub1604")

name = "ubuntu1604_influxdb_grafana"

j.actions.resetAll()

d.cuisine.apps.influxdb.build(start=False)
d.cuisine.apps.grafana.build(start=False)

# d.cuisine.installerdevelop.jumpscale8()

from IPython import embed
print ("DEBUG NOW sdsds")
embed()
p


# d.cuisine.core.dir_remove("$GODIR/src/*")
# d.cuisine.core.dir_remove("$TMPDIR/*")
# d.cuisine.core.dir_remove("$VARDIR/data/*")

# d.commit("jumpscale/%s" % name, delete=True, force=True)

# j.sal.btrfs.subvolumeCreate("/storage/builder")
# j.sal.btrfs.subvolumeCreate("/storage/builder/sandbox_ub1604")


# repos = [
#     'https://github.com/Jumpscale/ays_jumpscale8.git',
#     'https://github.com/Jumpscale/jumpscale_core8.git',
#     'https://github.com/JumpScale/jscockpit.git'
# ]

# for url in repos:
#     d.cuisine.git.pullRepo(url, ssh=False)

# d.cuisine.package.mdupdate()

# d.cuisine.core.file_copy('/usr/local/bin/jspython', '$BINDIR')

sandbox_script = """
cuisine = j.tools.cuisine.local
paths = []
paths.append("/usr/lib/python3.5/")
paths.append("/usr/local/lib/python3.5/dist-packages")
paths.append("/usr/lib/python3/dist-packages")

excludeFileRegex=["-tk/", "/lib2to3", "-34m-", ".egg-info"]
excludeDirRegex=["/JumpScale", "\.dist-info", "config-x86_64-linux-gnu", "pygtk"]

dest = j.sal.fs.joinPaths(cuisine.core.dir_paths['base'], 'lib')

for path in paths:
    j.tools.sandboxer.copyTo(path, dest, excludeFileRegex=excludeFileRegex, excludeDirRegex=excludeDirRegex)

if not j.sal.fs.exists("%s/bin/python" % cuisine.core.dir_paths['base']):
    j.sal.fs.copyFile("/usr/bin/python3.5", "%s/bin/python" % cuisine.core.dir_paths['base'])

j.tools.sandboxer.sandboxLibs("%s/lib" % cuisine.core.dir_paths['base'], recursive=True)
j.tools.sandboxer.sandboxLibs("%s/bin" % cuisine.core.dir_paths['base'], recursive=True)
"""
print("start sandboxing")
# d.cuisine.core.execute_jumpscript(sandbox_script)

name="stats"

copy_script="""
j.sal.fs.removeDirTree("/out/$name/jumpscale8/")
j.sal.fs.copyDirTree("/opt/jumpscale8/","/out/$name/jumpscale8",deletefirst=True,ignoredir=['.egg-info', '.dist-info','__pycache__'],ignorefiles=['.egg-info',"*.pyc"])
j.sal.fs.removeIrrelevantFiles("/out")
"""
copy_script=copy_script.replace("$name",name)
print("start copy sandbox")
# d.cuisine.core.execute_jumpscript(copy_script)


d = j.sal.docker.create(name='js8_stats',
                         stdout=True,
                         base='jumpscale/ubuntu1604',
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False,
                         vols="/out:/storage/builder/sandbox_ub1604")

print("create sandbox")

d.executor.sshclient.rsync_up("/storage/builder/sandbox_ub1604/stats/jumpscale8/","/opt/jumpscale8/")

s="""
set -ex
cd /opt/jumpscale8
source env.sh
js 'j.tools.console.echo("SUCCEEDED")'
"""
d.cuisine.core.execute_bash(s)

s="""
find -regex '.*__pycache__.*' -delete
rm -rf /var/log
mkdir -p /var/log/apt
rm -rf /var/tmp
mkdir -p /var/tmp
"""
d.cuisine.core.execute_bash(s)


add='source /opt/jumpscale8/env.sh'
prof=d.cuisine.core.file_read("/root/.profile")

if not add in prof:
    prof+='\n%s\n'%add
    d.cuisine.core.file_write("/root/.profile",prof)


d.commit("jumpscale/stats_server", delete=True, force=True)


from IPython import embed
print ("DEBUG NOW sdsds")
embed()
p

