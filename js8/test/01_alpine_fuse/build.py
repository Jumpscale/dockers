from JumpScale import j

j.actions.resetAll()

logger = j.logger.get('j.docker.alpine_aydofs')

d = j.sal.docker.create(name='build',
                        stdout=True,
                        base='jumpscale/alpine',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=False,
                        ssh=True,
                        sharecode=False,
                        setrootrndpasswd=False,
                        vols="/builder/:/storage/builder/sandbox_ub1604/js8")

config = '''\
[[mount]]
    path="/opt"
    flist="/etc/fs/js8_opt.flist"
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

# TODO: package manager should be aware of alpine pkg system
# d.cuisine.package.ensure('fuse')

d.cuisine.core.run('apk update')
d.cuisine.core.run('apk add fuse')

d.cuisine.core.file_copy('/builder/jumpscale8/bin/fs', '/usr/local/bin')
d.cuisine.core.dir_ensure('/etc/fs/')
d.cuisine.core.file_write('/etc/fs/config.toml', config)
d.cuisine.core.file_copy('/builder/md/js8_opt.flist', '/etc/fs/js8_opt.flist')

d.commit("jumpscale/alpine_aydofs", delete=True, force=True)