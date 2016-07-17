from JumpScale import j

j.actions.resetAll()

logger = j.logger.get('j.docker.sandbox_upload')
d = j.sal.docker.create(name='js8_host',
                        stdout=True,
                        base='jumpscale/ubuntu1604_sandbox',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        ports="22:7022 8090:8090",
                        sharecode=False,
                        setrootrndpasswd=False,
                        vols="/builder:/storage/builder/sandbox_ub1604/js8")

...
