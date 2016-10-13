
from JumpScale import j

j.data.cache.reset()  # make sure cache is gone


def resetAll():
    # DANGEROUS WILL CLEAN ALL LOCAL BTRFS VOLUMES
    j.sal.btrfs.subvolumesDelete("/storage/builder", filterExclude="/docker")
    j.sal.docker.destroyAll()
    j.sal.docker.removeImages()
    j.sal.process.execute("weave stop")
    j.sal.process.execute("weave reset")
    j.sal.process.execute("weave launch")


def base(push=True):

    # move to app in cuisine under apps and call from here
    def shellinabox(d):
        d.cuisine.package.install('shellinabox')
        bin_path = d.cuisine.bash.cmdGetPath('shellinaboxd')
        d.cuisine.core.file_copy(bin_path, "$binDir")

    j.sal.btrfs.subvolumeCreate("/storage/jstor")
    # j.sal.btrfs.subvolumeCreate("/storage/builder/sandbox_ub1604")

    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    # makes sure we build redis in stead of using from system which is default behaviour
    d.cuisine.apps.redis.install()

    # install base, python, pip3, ...
    d.cuisine.development.js8.installDeps()

    # call cuisine method
    shellinabox(d)

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_base", delete=True, force=True,
             push=push)


def jumpscale(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_base",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.development.js8.install(deps=False)
    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_js8", delete=True, force=True,
             push=push)


def mariadb(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_base",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False
                            )

    d.cuisine.apps.mariadb.install()

    cmd = "/usr/sbin/mysqld --basedir=/usr --datadir=/data/db \
--plugin-dir=/usr/lib/mysql/plugin --log-error=/dev/log/mysql/error.log \
--pid-file=/var/run/mysqld/mysqld.pid --socket=/var/run/mysqld/mysqld.sock --port=3306"

    d.cuisine.processmanager.ensure('mariadb', cmd)

    conf = {
        'volume': '/data/db',
        'expose': '3306',
    }

    d.commit("jumpscale/ubuntu1604_mariadb", delete=True, force=True,
             push=push, conf=conf)


def golang(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_js8",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.development.golang.install()
    d.cuisine.development.golang.install_godep()
    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_golang", delete=True, force=True,
             push=push)


def stats(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_golang",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.apps.mongodb.build(start=False)

    d.cuisine.apps.influxdb.install()

    d.cuisine.apps.grafana.build()

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_stats", delete=True, force=True,
             push=push)


def tidb(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_all",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.development.rust.install()
    d.cuisine.apps.tidb.build(install=True)
    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_all", delete=True, force=True,
             push=push)


def owncloud(push=True):
    d = j.sal.docker.create(name='owncloud',
                            stdout=True,
                            base="jumpscale/ubuntu1604_all",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.apps.nginx.build()
    d.cuisine.development.php.build()
    d.cuisine.development.php.install()
    d.cuisine.apps.owncloud.install(start=False)

    d.commit("jumpscale/ubuntu1604_all", delete=True, force=True,
             push=push)
    d.destroy()


def portal(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_stats",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.apps.portal.install(start=False)

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_portal", delete=True, force=True,
             push=push)


def all(push=True):
    d = j.sal.docker.create(name='build',
                            stdout=True,
                            base="jumpscale/ubuntu1604_portal",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.apps.caddy.install(start=False)

    d.cuisine.apps.geodns.install()

    d.cuisine.apps.brotli.build()
    d.cuisine.apps.brotli.install()

    d.cuisine.apps.redis.build()

    d.cuisine.development.lua.installLuaTarantool()

    d.cuisine.apps.syncthing.build(start=False)
    d.cuisine.apps.controller.build(start=False)
    d.cuisine.systemservices.g8oscore.build(start=False)

    d.cuisine.systemservices.g8osfs.build(start=False)
    d.cuisine.systemservices.aydostor.build(start=False)

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_all", delete=True, force=True,
             push=push)


def cockpit(push=True):
    d = j.sal.docker.create(name='build_phase2',
                            stdout=True,
                            base="jumpscale/ubuntu1604_all",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.solutions.cockpit.install(start=False)

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_cockpit", delete=True, force=True,
             push=push)


def ovs(push=True):
    d = j.sal.docker.create(name='build_phase2',
                            stdout=True,
                            base="jumpscale/ubuntu1604_all",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.apps.alba.build(start=False)
    d.cuisine.apps.volumedriver.build(start=False)

    d.cuisine.tools.sandbox.cleanup()
    d.commit("jumpscale/ubuntu1604_ovs", delete=True, force=True,
             push=push)


def scalityS3(push=True):
    d = j.sal.docker.create(name='build_scalityS3',
                            stdout=True,
                            base="jumpscale/ubuntu1604_all",
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False)

    d.cuisine.core.dir_ensure('/data/data')
    d.cuisine.core.dir_ensure('/data/meta')

    d.cuisine.apps.nodejs.install()
    d.cuisine.apps.s3server.install(storageLocation="/data/data", metaLocation="/data/meta/", start=False)

    d.cuisine.processmanager.ensure(
        name='scalityS3',
        cmd='npm run start_location',
        path='/opt/jumpscale8/apps/S3'
    )

    conf = {
        'volume': '/data',
        'expose': '8000',
    }

    d.commit("jumpscale/ubuntu1604_all", delete=True, force=True, push=push,
             conf=conf)

    d.destroy()


def sandbox(upload_to_stor=False):

    # create new docker to do the sandboxing in, needs to start from the development sandbox
    vols = "/storage/jstor:/storage/jstor/" if not upload_to_stor else ''
    d = j.sal.docker.create(name='sandboxer',
                            stdout=True,
                            base='jumpscale/ubuntu1604_all',
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False, weavenet=False,
                            vols=vols)

    # copy tools & update
    s = """
    set -ex
    cd /opt/code/github/jumpscale/jumpscale_core8/;git checkout . -f; git pull
    cd /opt/code/github/jumpscale/jumpscale_portal8/;git checkout . -f; git pull
    cd /opt/code/github/jumpscale/ays_jumpscale8/;git checkout . -f; git pull

    cd /opt/jumpscale8/bin
    cp /usr/local/bin/bro .
    cp /usr/bin/tarantool* .
    cp /usr/bin/lua* .
    cp /usr/local/bin/capnp* .
    cp /usr/local/lib/luarocks/rocks/lua-capnproto/0.1.3-1/bin/* .
    cp /usr/local/lib/luarocks/rocks/lua-cjson/2.1.0-1/bin/* .
    cp /usr/local/lib/libluajit-5.1.so .
    cp /usr/local/lib/lua/5.1/* .

    rsync -rv /usr/local/share/lua/5.1/ /opt/jumpscale8/lib/lua/
    rsync -rv /usr/local/share/luajit-2.1.0-beta2/ /opt/jumpscale8/lib/lua/

    mkdir -p /opt/jumpscale8/lib/lua/luarocks/
    rsync -rv /usr/share/lua/5.1/luarocks/ /opt/jumpscale8/lib/lua/luarocks/

    mkdir -p /opt/jumpscale8/lib/lua/tarantool/
    rsync -rv /usr/share/tarantool/ /opt/jumpscale8/lib/lua/tarantool/

    """
    d.cuisine.core.execute_bash(s)

    js_script = """
    paths = []
    paths.append("/usr/lib/python3/dist-packages")
    paths.append("/usr/lib/python3.5/")
    paths.append("/usr/local/lib/python3.5/dist-packages")

    base_dir = j.tools.cuisine.local.core.dir_paths['base']
    dest = j.sal.fs.joinPaths(base_dir, 'lib')

    excludeFileRegex = ["-tk/", "/lib2to3", "-34m-", ".egg-info", "lsb_release"]
    excludeDirRegex = ["/JumpScale", "\.dist-info", "config-x86_64-linux-gnu", "pygtk"]

    for path in paths:
        j.tools.sandboxer.copyTo(path, dest, excludeFileRegex=excludeFileRegex, excludeDirRegex=excludeDirRegex)

    j.tools.sandboxer.copyTo('/usr/local/bin/', '%s/bin/' % base_dir, excludeFileRegex=excludeFileRegex, excludeDirRegex=excludeDirRegex)

    if not j.sal.fs.exists("%s/bin/python" % base_dir):
        j.sal.fs.symlink("%s/bin/python3" % base_dir, "%s/bin/python3.5" % base_dir, overwriteTarget=True)

    j.tools.sandboxer.sandboxLibs("%s/lib" % base_dir, recursive=True)
    j.tools.sandboxer.sandboxLibs("%s/bin" % base_dir, recursive=True)

    """
    d.cuisine.core.execute_jumpscript(js_script)

    if upload_to_stor:
        if not '/root/.ssh/ovh_rsa' in j.do.listSSHKeyFromAgent():
            raise RuntimeError('ovh key must be loaded to push to stor')
        stor = d._executor.jumpto('stor.jumpscale.org', identityfile='/home/reem/work/ovh_rsa')
        sp = stor._cuisine.tools.stor.getStorageSpace('sandbox_ub1604')
    else:
        sp = d.cuisine.tools.stor.getStorageSpace('sandbox_ub1604')

    sp.upload('opt', source='/opt')
    # remove docker
    d.destroy()


def build_docker_fromsandbox(push):
    """
    rsync files back after sandbox to a small ubuntu
    """

    d = j.sal.docker.create(name='js8_sandbox',
                            stdout=True,
                            base='jumpscale/ubuntu1604',
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            sharecode=False,
                            setrootrndpasswd=False,
                            vols="/storage/jstor:/storage/jstor/")

    print("create sandbox")

    # d.executor.sshclient.rsync_up("/storage/jstor/", "/opt/jumpscale8/")

    s = """
    set -ex
    cd /opt/jumpscale8
    source env.sh
    js 'j.tools.console.echo("SUCCEEDED")'
    """
    d.cuisine.core.execute_bash(s)

    add = 'source /opt/jumpscale8/env.sh'
    prof = d.cuisine.core.file_read("/root/.profile")

    if not add in prof:
        prof += '\n%s\n' % add
        d.cuisine.core.file_write("/root/.profile", prof)

    # clean stuff we don't need
    # d.cuisine.tools.sandbox.cleanup()

    d.commit("jumpscale/ubuntu1604_sandbox", delete=True, force=True,
             push=push)
    print("sandbox docker committed")


def storhost():
    namespace = 'sandbox_ub1604'

    d = j.sal.docker.create(name='g8stor',
                            stdout=True,
                            base='jumpscale/ubuntu1604_sandbox',
                            nameserver=['8.8.8.8'],
                            replace=True,
                            myinit=True,
                            ssh=True,
                            ports="22:7022 8090:8090",
                            sharecode=False,
                            setrootrndpasswd=False, weavenet=True,
                            vols="/mnt/aydostorx/:/storage/jstor/".format(namespace=namespace))

    CONFIG = """
    listen_addr = "0.0.0.0:8090"
    store_root = "/mnt/aydostorx/"
    """

    d.cuisine.core.dir_ensure("/mnt/aydostorx/fixed")
    d.cuisine.core.dir_ensure("/mnt/aydostorx/tmp")

    d.cuisine.core.file_write("/etc/js_storx.toml", CONFIG)

    pm = d.cuisine.processmanager.get(pm="tmux")
    cmd = "./stor -c /etc/js_storx.toml"
    pm.ensure(name="g8stor", cmd=cmd, env={}, path='/opt/jumpscale8/bin', descr='')

    # d.cuisine.processmanager.ensure('g8stor', cmd, path='/opt/jumpscale8/bin')

    if not j.sal.nettools.tcpPortConnectionTest("localhost", 8090):
        raise RuntimeError("cannot connect over tcp to port 8090 on localhost")

    d.commit("jumpscale/g8stor", delete=True, force=True, push=False)

    d = j.sal.docker.create(name="g8stor",
                            stdout=True,
                            base='jumpscale/g8stor',
                            nameserver=['8.8.8.8'],
                            replace=True,
                            ssh=True,
                            ports="22:7032 8090:8090",
                            privileged=True,
                            setrootrndpasswd=False,
                            weavenet=True,
                            vols="/mnt/aydostorx/namespaces/{namespace}:/storage/jstor/files".format(namespace=namespace))

    if not j.sal.nettools.tcpPortConnectionTest("localhost", 8090):
        raise RuntimeError("cannot connect over tcp to port 8090 on localhost after launching g8stor in docker.")


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
                            vols="/storage/jstor/:/storage/jstor/")

    config = """
    [[mount]]
         path="/opt"
         flist="/optvar/cfg/fs/js8_opt.flist"
         backend="main"
         #stor="stor1"
         mode = "OL"
         trim_base = true

    [backend.main]
        path="/tmp/aysfs_main"
        stor="stor1"
        #namespace="testing"
        namespace="dedupe"

        upload=true
        encrypted=false
        # encrypted=true
        user_rsa="user.rsa"
        store_rsa="store.rsa"

        aydostor_push_cron="@every 1m"
        cleanup_cron="@every 1m"
        cleanup_older_than=1 #in hours

    [aydostor.stor1]
        addr="http://g8stor:8090"
        #addr="http://192.168.0.182:8080/"
        login=""
        passwd=""
    """

    d.cuisine.package.ensure('fuse')
    #
    # d.cuisine.core.file_copy('/storage/jumpscale8/bin/fs', '/usr/local/bin')
    d.cuisine.core.dir_ensure('/optvar/cfg/fs/')
    d.cuisine.core.file_write('/optvar/cfg/fs/config.toml', config)
    d.cuisine.core.file_copy('/storage/jstor/flist/sandbox_ub1604/opt.flist', '/optvar/cfg/fs/js8_opt.flist')

    d.cuisine.tools.sandbox.cleanup()

    pm = d.cuisine.processmanager.get(pm="tmux")
    pm.ensure('g8fs', '/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')
    # d.cuisine.processmanager.ensure('g8fs', cmd='/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')

    d.commit("jumpscale/g8fs", delete=True, force=True, push=False)

    d.destroy()

    d = j.sal.docker.create(name="g8fs",
                            stdout=True,
                            base='jumpscale/g8fs',
                            nameserver=['8.8.8.8'],
                            myinit=True,
                            replace=True,
                            ports="22:7033",
                            ssh=True,
                            privileged=True,
                            setrootrndpasswd=True,
                            weavenet=True)

    s = """
        set -ex
        cd /opt/jumpscale8
        source env.sh
        js 'j.tools.console.echo("SUCCEEDED")'
        """
    d.cuisine.core.execute_bash(s)


def enableWeave():
    # IS NOT WORKING #TODO: *1
    j.sal.docker.weaveInstall(ufw=True)

# resetAll()

push = True

base(push=push)
print("******BASE DONE******")

jumpscale(push=push)
print("******JUMPSCALE DONE******")

golang(push=push)
print("******GOLANG DONE******")

stats(push=push)
print("******STATS DONE******")

portal(push=push)
print("******PORTAL DONE******")

all(push=push)
print("******ALL DONE******")

scalityS3(push=push)
print("******SCALITYS3 DONE******")

tidb(push=push)
print("******TIDB DONE******")

owncloud(push=push)
print("******OWNCLOUD DONE******")

cockpit(push=push)
print("******COCKPIT DONE******")

# ovs(push=push)
sandbox(upload_to_stor=False)
print("******SANDBOX DONE******")

# will create a docker where all sandboxed files are in, can be used without the js8_fs

# build_docker_fromsandbox(push=push)
# print("******BUILD DOCKER FROM SANDBOX DONE******")

# host a docker which becomes the host for our G8OS FS
storhost()
print("******STORHOST DONE******")

# now connect to our G8OS STOR
js8fs()
print("******JS8FS DONE******")
