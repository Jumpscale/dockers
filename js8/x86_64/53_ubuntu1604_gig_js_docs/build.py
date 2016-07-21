from JumpScale import j

name = 'ubuntu1604_git_js_docs'
logger = j.logger.get('j.docker.sandboxer')

# base='jumpscale/ubuntu1604_volumedriver'
base='jumpscale/ubuntu1604_gitbook'
j.sal.btrfs.subvolumeCreate("/storage/builder/docs")

d = j.sal.docker.create(name=name,
                         stdout=True,
                         base=base,
                         vols='/var/output:/storage/builder/docs',
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False)

j.actions.resetAll()

repos = {
    'IAAS - Compute = OpenVCloud': 'https://github.com/0-complexity/doc_openvcloud_public.git',
    'IAAS - Storage = OpenVStorage': 'https://github.com/openvstorage/ovs-documentation.git',
    'Automation Framework = Jumpscale': 'https://github.com/Jumpscale/jumpscale_core8.git',
    'Overlay Mgmt Platform = Cockpit': 'https://github.com/JumpScale/jscockpit.git',
    'Identity Management = ItsYouOnline': 'https://github.com/0-complexity/itsyouonline-reference-implementation.git',
}
#prob need more repo's

for name, url in repos.items():
    try:
        repo = d.cuisine.git.pullRepo(url, ssh=False)
        d.cuisine.core.run('gitbook install %s' % repo)
        d.cuisine.core.run('gitbook pdf "%s" "/var/output/%s.pdf"' % (repo, name))
    except Exception as e:
        logger.warn('Failed to build %s: %s' % (url, e))
