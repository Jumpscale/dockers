from JumpScale import j

name = "ubuntu1604_g8os_test"
j.actions.resetAll()

logger = j.logger.get('j.docker.sandbox_upload')

d = j.sal.docker.create(name='js8_host',
                        stdout=True,
                        base='jumpscale/ubuntu1604',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        ports="22:7022 8090:8090",
                        sharecode=False,
                        setrootrndpasswd=False,
                        vols="/builder:/storage/builder/sandbox_ub1604/js8")

d.cuisine.package.ensure('fuse')

d.cuisine.core.file_copy('/builder/jumpscale8/bin/fs', '/usr/local/bin')
d.cuisine.core.dir_ensure('/optvar/cfg/fs/')
d.cuisine.core.file_copy('/builder/jumpscale8/templates/cfg/fs/config.toml', '/optvar/cfg/fs/config.toml')
d.cuisine.core.file_copy('/builder/md/js8_opt.flist', '/optvar/cfg/fs/js8_opt.flist')

d.cuisine.processmanager.ensure('g8fs', '/usr/local/bin/fs -c /optvar/cfg/fs/config.toml')

d.commit("jumpscale/%s" % name, delete=True, force=True)