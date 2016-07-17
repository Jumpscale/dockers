from JumpScale import j

name = "ubuntu1604_python3"

j.actions.resetAll()

# j.do.createDir("/tmp/build")
# vols = '/bd_build:%s#/build:/tmp/build' % j.sal.fs.getcwd()
# print(vols)

d = j.sal.docker.create(name='build',
                        ports='',
                        vols='',
                        volsro='',
                        stdout=True,
                        base='jumpscale/ubuntu1604',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        cpu=None,
                        mem=0,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False)


d.cuisine.installer.base()

from IPython import embed
print ("DEBUG NOW sdsds")
embed()
p


d.cuisine.installerdevelop.python()
d.cuisine.installerdevelop.pip()
d.cuisine.installerdevelop.installJS8Deps()

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

d.cuisine.installerdevelop.cleanup()

d.commit("jumpscale/%s" % name, delete=True, force=True)
