
from JumpScale import j


def docker(reset=False):
    if reset:
        j.actions.resetAll()

    j.sal.btrfs.subvolumeCreate("/storage/builder")
    j.sal.btrfs.subvolumeCreate("/storage/builder/sandbox_ub1604")

    d = j.sal.docker.create(name='build_base',
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
    d.cuisine.installer.base()
    d.cuisine.installerdevelop.python()
    d.cuisine.installerdevelop.pip()
    d.cuisine.installerdevelop.installJS8Deps()

    if reset:
        d.cuisine.installerdevelop.cleanup()
        d.commit("jumpscale/ubuntu1604_js", delete=True, force=True,push=push)

def shellinabox():
    d.cuisine.package.install('shellinabox')
    bin_path = d.cuisine.bash.cmdGetPath('shellinaboxd')
    d.cuisine.core.file_copy(bin_path, "$binDir")

def cleanup(aggressive=False,cuisine=None):
    if cuisine!=None:
        d=cuisine   
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

    if aggressive:
        C="""
        set -ex
        cd /
        find -regex '.*__pycache__.*' -delete
        rm -rf /var/log
        mkdir -p /var/log/apt
        rm -rf /var/tmp
        mkdir -p /var/tmp
        rm -rf /usr/share/doc
        mkdir -p /usr/share/doc
        rm -rf /usr/share/gcc-5
        rm -rf /usr/share/gdb
        rm -rf /usr/share/gitweb
        rm -rf /usr/share/info
        rm -rf /usr/share/lintian
        rm -rf /usr/share/perl
        rm -rf /usr/share/perl5
        rm -rf /usr/share/pyshared
        rm -rf /usr/share/python*
        rm -rf /usr/share/zsh

        rm -rf /usr/share/locale-langpack/en_AU
        rm -rf /usr/share/locale-langpack/en_CA
        rm -rf /usr/share/locale-langpack/en_GB
        rm -rf /usr/share/man

        rm -rf /usr/lib/python*
        rm -rf /usr/lib/valgrind

        rm -rf /usr/bin/python*
        """
        d.cuisine.core.run_script(C)

def sandbox(d):

    #copy brotli compression tool
    s="""
    set -ex
    cd /opt/jumpscale8/bin
    cp /usr/local/bin/bro .
    """
    d.cuisine.core.run_script(s)

    d.cuisine.sandbox.do("/out")

def sandbox_docker(push):


    d = j.sal.docker.create(name='js8_sandbox',
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

    d.executor.sshclient.rsync_up("/storage/builder/sandbox_ub1604/js8/jumpscale8/","/opt/jumpscale8/")

    s="""
    set -ex
    cd /opt/jumpscale8
    source env.sh
    js 'j.tools.console.echo("SUCCEEDED")'
    """
    d.cuisine.core.run_script(s)

    add='source /opt/jumpscale8/env.sh'
    prof=d.cuisine.core.file_read("/root/.profile")

    if not add in prof:
        prof+='\n%s\n'%add
        d.cuisine.core.file_write("/root/.profile",prof)

    #clean stuff we don't need
    cleanup(aggressive=False,cuisine=d)

    d.commit("jumpscale/ubuntu1604_sandbox", delete=True, force=True,push=push)
    print("sandbox docker committed")

def storhost():
    namespace = 'js8_opt'

    d = j.sal.docker.create(name='g8stor',
                        stdout=True,
                        base='jumpscale/ubuntu1604_sandbox',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        ports="22:7022 8090:8090",
                        sharecode=False,
                        setrootrndpasswd=False,weavenet=True,
                        vols="/mnt/aydostorx/namespaces/{namespace}:/storage/builder/sandbox_ub1604/js8/files".format(namespace=namespace))

    CONFIG = """
    listen_addr = "0.0.0.0:8090"
    store_root = "/mnt/aydostorx/"
    """

    d.cuisine.core.dir_ensure("/mnt/aydostorx/fixed")
    d.cuisine.core.dir_ensure("/mnt/aydostorx/tmp")

    d.cuisine.core.file_write("/etc/js_storx.toml", CONFIG)

    pm = d.cuisine.processmanager.get(pm="tmux")
    cmd="./stor -c /etc/js_storx.toml"
    pm.ensure(name="storx", cmd=cmd, env={}, path='/opt/jumpscale8/bin', descr='')

    if not j.sal.nettools.tcpPortConnectionTest("localhost", 8090):
        raise RuntimeError("cannot connect over tcp to port 8090 on localhost")

def js8fs():

    name = "ubuntu1604_g8os_base"
    j.actions.resetAll()

    d = j.sal.docker.create(name=name,
                            stdout=True,
                            base='jumpscale/ubuntu1604',
                            nameserver=['8.8.8.8'],
                            replace=True,
                            ssh=True,
                            privileged=True,
                            setrootrndpasswd=False,
                            weavenet=True,
                            vols="/builder:/storage/builder/sandbox_ub1604/js8")

    config = '''\
    [[mount]]
        path="/opt"
        flist="/optvar/cfg/fs/js8_opt.flist"
        backend="opt"
        mode="RO"
        trim_base=true
    [backend]
    [backend.opt]
        path="/optvar/fs_backend/opt"
        stor="public"
        namespace="js8_opt"
        cleanup_cron="@every 1h"
        cleanup_older_than=24
        log=""
    [aydostor]
    [aydostor.public]
        #use the IP of the docker host.
        addr="http://172.17.0.1:8090"
        login=""
        passwd=""
    '''
    d.cuisine.package.ensure('fuse')

    d.cuisine.core.file_copy('/builder/jumpscale8/bin/fs', '/usr/local/bin')
    d.cuisine.core.dir_ensure('/optvar/cfg/fs/')
    d.cuisine.core.file_write('/optvar/cfg/fs/config.toml', config)
    d.cuisine.core.file_copy('/builder/md/js8_opt.flist', '/optvar/cfg/fs/js8_opt.flist')

    cleanup(aggressive=True,cuisine=d)

    pm = d.cuisine.processmanager.get(pm="tmux")
    pm.ensure('g8fs', '/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')
    # d.cuisine.processmanager.ensure('g8fs', '/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')

    # d.commit("jumpscale/%s" % name, delete=True, force=True)


def enableWeave():
    j.sal.docker.weaveInstall(ufw=True)

    

#### ARGS
push=True
reset=False


#### MAIN

d=docker(reset=reset)

# base(push=push,reset=reset)

# shellinabox()

# d.cuisine.installerdevelop.jumpscale8()
# if reset:
#     cleanup(cuisine=d)
#     d.commit("jumpscale/ubuntu1604_js8", delete=True, force=True,push=True)

# d.cuisine.golang.install(force=True)

# if reset: #can only commit/push when we stared from clean slate
#     cleanup(cuisine=d)
#     d.commit("jumpscale/ubuntu1604_golang", delete=True, force=True,push=True)

# d.cuisine.apps.caddy.install(start=False)

# d.cuisine.apps.portal.install(start=False)
# d.cuisine.apps.mongodb.build(start=False)

# d.cuisine.apps.grafana.build(start=False)
d.cuisine.apps.controller.build(start=False)
d.cuisine.apps.core.build(start=False)

# d.cuisine.apps.stor.build(start=False)
# d.cuisine.apps.cockpit.build(start=False)

# d.cuisine.apps.influxdb.install()  

# d.cuisine.geodns.install()

# d.cuisine.lua.install_lua_tarantool()

# d.cuisine.apps.fs.build(start=False)

cleanup(cuisine=d)
#this is the full one, we can commit
d.commit("jumpscale/ubuntu1604_js_development", delete=True, force=True,push=True)

#start from committed js_development docker
d = j.sal.docker.create(name='build',base="jumpscale/ubuntu1604_js_development",replace=True,ssh=True,setrootrndpasswd=False,vols="/out:/storage/builder/sandbox_ub1604")

sandbox(d)

#will create a docker where all sandboxed files are in, can be used without the js8_fs
sandbox_docker(push=push)

#host a docker which becomes the host for our js8
#@todo next don't work
storhost()
js8fs()



