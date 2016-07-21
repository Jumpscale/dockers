from JumpScale import j

name = "ubuntu1604_g8os_test"
j.actions.resetAll()

logger = j.logger.get('j.docker.sandbox_upload')

d = j.sal.docker.create(name='g8os-fs',
                        stdout=True,
                        base='jumpscale/ubuntu1604',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False,
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

d.cuisine.processmanager.ensure('g8fs', '/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')

d.commit("jumpscale/%s" % name, delete=True, force=True)