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

# make sure brotli is installed
if not d1.cuisine.core.command_check('bro'):
    bro_script = """
    cd $tmpDir; git clone https://github.com/google/brotli.git
    cd $tmpDir/brotli/
    python setup.py install
    make bro
    cp bin/bro $binDir/bro
    """
    d1.cuisine.core.run_script(bro_script)

d1.cuisine.core.file_copy('/usr/local/bin/jspython', '$binDir')

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
logger.info("start sandboxing")
d1.cuisine.core.execute_jumpscript(sandbox_script)

name="js8"

dedupe_script = """
j.sal.fs.removeDirTree("/out/$name")
j.tools.sandboxer.dedupe('/opt', storpath='/out/$name', name='js8_opt', reset=False, append=True, excludeDirs=['/opt/code'])
"""
dedupe_script=dedupe_script.replace("$name",name)
logger.info("start dedupe")
d1.cuisine.core.execute_jumpscript(dedupe_script)


copy_script="""
j.sal.fs.removeDirTree("/out/$name/jumpscale8/")
j.sal.fs.copyDirTree("/opt/jumpscale8/","/out/$name/jumpscale8",deletefirst=True,ignoredir=['.egg-info', '.dist-info','__pycache__'],ignorefiles=['.egg-info',"*.pyc"])
j.sal.fs.removeIrrelevantFiles("/out")
"""
copy_script=copy_script.replace("$name",name)
logger.info("start copy sandbox")
d1.cuisine.core.execute_jumpscript(copy_script)

# logger.info("commit image jumpscale/%s" % name)
# d1.commit("jumpscale/%s" % name, delete=True, force=True)
