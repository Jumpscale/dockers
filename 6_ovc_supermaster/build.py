from JumpScale import j


j.do.createDir("/tmp/build")
vols='/code:%s#/build:/tmp/build'%j.sal.fs.getcwd()

#d=j.sal.docker.create(name='build', ports='', vols=vols, volsro='', stdout=True, base='jumpscale/ubuntu1510_golang', nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0, jumpscale=False, ssh=True, myinit=True, sharecode=True)
d=j.sal.docker.get('build')
#prepare ubuntu with right apt repo's (should move to the base to start from)


items=j.sal.fs.listDirsInDir("services",False,True)
items.sort()

for item in items:
    d.cuisine.run("bash /code/services/%s/%s.sh"%(item,item))

from IPython import embed
embed()