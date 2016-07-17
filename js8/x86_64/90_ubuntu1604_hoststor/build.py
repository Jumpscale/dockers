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


from IPython import embed
print ("DEBUG NOW sdsd")
embed()
p


store_client.putFile("test","/storage/builder/sandbox_ub1604/js8/files/a/a/aa6a634cf373728e934b3d6da15759bd.bro")



sandbox_dir = '/optvar/tmp/sandboxing'  # has to be the same as the one define in 80_sandbox docker
store_addr = 'https://stor.jumpscale.org/storx'
namespace = 'js8_opt'

upload_script = """
store_client = j.clients.storx.get('{store_addr}')
files_path = j.sal.fs.joinPaths('{sandbox_dir}', 'files')
files = j.sal.fs.listFilesInDir(files_path, recursive=True)
error_files = []
for f in files:
    src_hash = j.data.hash.md5(f)
    print('uploading %s' % f)
    uploaded_hash = store_client.putFile('{namespace}', f)
    if src_hash != uploaded_hash:
        error_files.append(f)
        print("%s hash doesn't match\\nsrc     :%32s\\nuploaded:%32s" % (f, src_hash, uploaded_hash))

if len(error_files) == 0:
    print("all uploaded ok")
else:
    raise RuntimeError('some files didnt upload properly. %s' % ("\\n".join(error_files)))

metadataPath = j.sal.fs.joinPaths('{sandbox_dir}', "md", "{namespace}.flist")
print('uploading %s' % metadataPath)
store_client.putStaticFile("{namespace}.flist", metadataPath)
""".format(store_addr=store_addr, sandbox_dir=sandbox_dir, namespace=namespace)

logger.debug(upload_script)
logger.debug('Start upload to store %s' % store_addr)
d.cuisine.core.execute_jumpscript(upload_script)
