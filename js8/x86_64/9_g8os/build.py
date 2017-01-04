from JumpScale import j

name = "g8os"


d = j.sal.docker.create(
    name='build',
    ports='',
    stdout=True,
    base='jumpscale/ubuntu1604_golang',
    nameserver=['8.8.8.8'],
    replace=True,
    cpu=None,
    mem=0,
    ssh=True,
    sharecode=False,setrootrndpasswd=False)

cuisine = d.cuisine

cuisine.apps.core.build()
# now, package core

cuisine.core.dir_ensure('/usr/bin/')
cuisine.core.dir_ensure('/etc/g8os/g8os.d/')
cuisine.core.dir_ensure('/usr/lib/g8os/')
cuisine.core.dir_ensure('/var/log/g8os/')

# binaries
cuisine.core.file_copy('$BINDIR/core', '/usr/bin/')

sourcepath = "$GOPATHDIR/src/github.com/g8os/core"

cuisine.core.file_copy('%s/init' % (sourcepath), '/usr/bin/init')
cuisine.core.run('chmod a+x /usr/bin/init')

# configurations
cuisine.core.file_copy(
    '%s/{g8os.toml,network.toml}' %
    (sourcepath), '/etc/g8os/')
cuisine.core.file_copy('%s/conf/*' % (sourcepath), '/etc/g8os/g8os.d/')

cuisine.core.file_copy(
    '%s/conf.extra/*-ubuntu.toml' %
    (sourcepath), '/etc/g8os/g8os.d/')

# extensions
cuisine.core.file_copy(
    '%s/extensions' %
    (sourcepath),
    '/usr/lib/g8os/',
    recursive=True)
cuisine.core.dir_ensure('/usr/lib/g8os/extensions/syncthing')
cuisine.core.file_copy(
    '$BINDIR/syncthing',
    '/usr/lib/g8os/extensions/syncthing')

# corectl
cuisine.golang.clean_src_path()
cuisine.golang.get('github.com/g8os/corectl')
cuisine.core.file_copy('$GOPATHDIR/bin/corectl', '/usr/bin/corectl')

cuisine.core.file_unlink(
    '/etc/g8os/g8os.d/{agetty-ubuntu.toml,modprobe.toml,udev-ubuntu.toml,basic.jumpscripts.toml}')
cuisine.core.run("perl -i -pe 's/^.*network\.toml.*$//' /etc/g8os/g8os.toml")

d.commit(
    "jumpscale/%s" %
    name,
    delete=True,
    force=True,
    conf={
        'CMD': [
            '/usr/bin/core',
            '-nid',
            '1',
            '-gid',
            '1',
            '-roles',
            'g8os']})
