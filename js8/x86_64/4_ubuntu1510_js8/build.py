from JumpScale import j


j.do.createDir("/tmp/build/opt/jumpscale8")
vols='/bd_build:%s#/build:/tmp/build'%curdir
print (vols)

d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510_python3', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=False)
# d=j.sal.docker.get('build')



JS="""
#!/bin/bash
set -e
source /bd_build/buildconfig
set -x

export SANDBOX=0
cd /tmp;rm -f install.sh;curl -k https://raw.githubusercontent.com/Jumpscale/jumpscale_core8/master/install/install.sh > install.sh;bash install.sh

"""
def js():
    d.cuisine.run_script(JS)
j.actions.start(js, runid='ubuntu1510_js8')

# CLEANUP='''
# #!/bin/bash
# set -e
# source /bd_build/buildconfig
# set -x

# set +ex
# apt-get clean
# rm -rf /var/tmp/*
# # rm -rf /var/lib/apt/lists/*
# rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup
# rm -f /etc/ssh/ssh_host_*

# '''
# d.cuisine.run_script(CLEANUP)
