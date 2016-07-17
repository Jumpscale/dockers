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
                        vols="/out:/storage/builder/sandbox_ub1604")

CONFIG="""
listen_addr="localhost:8090"
store_root="/mnt/openvcloud/aydostorx"
#sources=["http://localhost:8081"]
#authentification="auth.toml"
#[tls]
#certificate="cert.pem"
#key="key.rsa"
"""

d.cuisine.core.dir_ensure("/out/aydostorx/fixed")
d.cuisine.core.dir_ensure("/out/aydostorx/namespaces")
d.cuisine.core.dir_ensure("/out/aydostorx/tmp")

d.cuisine.core.file_write("/etc/js_storx.toml",CONFIG)

#can be removed is already in sandbox build
add='source /opt/jumpscale8/env.sh'
prof=d.cuisine.core.file_read("/root/.profile")

if not add in prof:
    prof+='\n%s\n'%add
    d.cuisine.core.file_write("/root/.profile",prof)


pm=d.cuisine.processmanager.get(pm="tmux")

cmd="./stor -c /etc/js_storx.toml"
pm.ensure(name="storx", cmd=cmd, env={}, path='/opt/jumpscale8/bin', descr='')

if not j.sal.nettools.tcpPortConnectionTest("localhost",8090):
    raise RuntimeError("cannot connect over tcp to port 8090 on localhost")

store_client = j.clients.storx.get('http://localhost:8090')

#@todo PLEASE COMPLETE

from IPython import embed
print ("DEBUG NOW sdsd")
embed()
p

#do a test
store_client.putFile("test","/storage/builder/sandbox_ub1604/js8/files/a/a/aa6a634cf373728e934b3d6da15759bd.bro")

