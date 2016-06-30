from JumpScale import j

logger = j.logger.get('j.docker.sandbox_upload')
d = j.sal.docker.create(name='sandbox_upload',
                        stdout=True,
                        base='jumpscale/ubuntu1604_sandbox',
                        nameserver=['8.8.8.8'],
                        replace=True,
                        myinit=True,
                        ssh=True,
                        sharecode=False)


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

metadataPath = j.sal.fs.joinPaths(output_dir, "md", "%s.flist" % namespace)
print('uploading %s' % metadataPath)
store_client.putStaticFile(namespace+".flist", metadataPath)
""".format(store_addr=store_addr, sandbox_dir=sandbox_dir, namespace=namespace)

logger.debug(upload_script)
logger.debug('Start upload to store %s' % store_addr)
d.cuisine.core.execute_jumpscript(upload_script)
