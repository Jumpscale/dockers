from JumpScale import j

j.actions.resetAll()

namespace = 'js8_opt'

logger = j.logger.get('j.docker.sandbox_upload')
d = j.sal.docker.create(name='storx',
                        stdout=True,
                        base='jumpscale/ubuntu1604_sandbox',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        ports="22:7022 8090:8090",
                        sharecode=False,
                        setrootrndpasswd=False,
                        vols="/mnt/aydostorx/namespaces/{namespace}:/storage/builder/sandbox_ub1604/js8/files".format(namespace=namespace))

CONFIG = """
listen_addr = "0.0.0.0:8090"
store_root = "/mnt/aydostorx/"
"""

d.cuisine.core.dir_ensure("/mnt/aydostorx/fixed")
d.cuisine.core.dir_ensure("/mnt/aydostorx/tmp")

d.cuisine.core.file_write("/etc/js_storx.toml", CONFIG)

pm = d.cuisine.processmanager.get(pm="tmux")

cmd="./stor -c /etc/js_storx.toml"
pm.ensure(name="storx", cmd=cmd, env={}, path='/opt/jumpscale8/bin', descr='')

if not j.sal.nettools.tcpPortConnectionTest("localhost", 8090):
    raise RuntimeError("cannot connect over tcp to port 8090 on localhost")
