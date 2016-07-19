from JumpScale import j

name = 'ubuntu1604_gitbook'
logger = j.logger.get('j.docker.sandboxer')

# base='jumpscale/ubuntu1604_volumedriver'
base='jumpscale/ubuntu1604_js8_development'

d = j.sal.docker.create(name='build',
                         stdout=True,
                         base=base,
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False)

j.actions.resetAll()

d.cuisine.package.ensure('calibre-bin')
d.cuisine.package.ensure('nodejs')
d.cuisine.package.ensure('npm')
d.cuisine.core.run('npm install -g gitbook-cli')
d.cuisine.core.run('ln -s /usr/bin/nodejs /usr/bin/node')
d.cuisine.core.run('gitbook update')

d.commit("jumpscale/%s" % name, delete=True, force=True)
