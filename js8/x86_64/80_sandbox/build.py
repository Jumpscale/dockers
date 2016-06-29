from JumpScale import j


d=j.sal.docker.create(name='build_ub', ports='', stdout=True, base='jumpscale/ubuntu1604_jscockpit', \
    nameserver=['8.8.8.8'],replace=True, cpu=None, mem=0,  ssh=True,sharecode=False)


d2=j.sal.docker.create(name='build_alpine', ports='', stdout=True, base='jumpscale/alpine', nameserver=['8.8.8.8'],\
    replace=True, cpu=None, mem=0, ssh=True,sharecode=False)



from IPython import embed
print ("DEBUG NOW sdsd")
embed()
p

print ("SANDBOX")
SANDBOX='''
d=j.atyourservice.debug.get("main")
d.addSandboxSource("/usr/bin/rsync")
d.sandbox()
'''
d.cuisine.core.run_script(SANDBOX)


COPY="""
j.do.delete("/build/opt/jumpscale8/")
j.do.delete("/build/optvar/")
j.do.copyTree("/opt/jumpscale8/","/build/opt/jumpscale8/")
j.do.copyTree("/optvar/","/build/optvar/")
j.do.delete("/build/opt/jumpscale8/bin/metadata.db")
"""
d.cuisine.core.run_script(copy)
