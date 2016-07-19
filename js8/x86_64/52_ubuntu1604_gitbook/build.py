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

#@todo complete ...