from JumpScale import j

name = 'ubuntu1604_sanbox'
logger = j.logger.get('j.docker.sandboxer')

d1 = j.sal.docker.create(name='build_sandbox',
                         stdout=True,
                         base='jumpscale/g8cockpit',
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False)


d2 = j.sal.docker.create(name='build_alpine',
                         stdout=True,
                         base='jumpscale/alpine',
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=False,
                         ssh=True,
                         sharecode=False)


# Sandbox need to happens in two step
# first we copy all required libs and binaries under /opt/jumpscale8
# second we dedupe all the files and generated the flist.
# These two steps needs to happens in two script, doing it all in one script segfault.

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


dedupe_script = """
j.tools.sandboxer.dedupe('/opt', storpath='/optvar/tmp/sandboxing', name='js8_opt', reset=True, append=True, excludeDirs=['/opt/code'])
"""
logger.info("start dedupe")
d1.cuisine.core.execute_jumpscript(dedupe_script)


# TODO: send sandbox on alpine and try to start jumpscale. Currently aline can't load the librairies from ubuntu1604

logger.info("commit image jumpscale/%s" % name)
d1.commit("jumpscale/%s" % name, delete=True, force=True)
