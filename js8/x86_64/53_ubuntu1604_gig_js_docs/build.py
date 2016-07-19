from JumpScale import j

output_dir = "/opt/docs/"
j.sal.fs.createDir(output_dir)

name = 'ubuntu1604_gitbook'
logger = j.logger.get('j.docker.sandboxer')

# base='jumpscale/ubuntu1604_volumedriver'
base='jumpscale/ubuntu1604_gitbook'

d = j.sal.docker.create(name='build',
                         stdout=True,
                         base=base,
                         vols='/var/output:%s' % output_dir,
                         nameserver=['8.8.8.8'],
                         replace=True,
                         myinit=True,
                         ssh=True,
                         sharecode=False,
                         setrootrndpasswd=False)

repos = {
    'Automation Framework = Jumpscale': 'https://github.com/Jumpscale/jumpscale_core8.git',
    'Overlay Mgmt Platform = Cockpit': 'https://github.com/JumpScale/jscockpit.git'
}
#prob need more repo's

for name, url in repos.items():
    try:
        repo = d.cuisine.git.pullRepo(url, ssh=False)
        d.cuisine.core.run('gitbook install %s' % repo)
        d.cuisine.core.run('gitbook pdf %s /var/output/%s.pdf' % (repo, name))
    except Exception as e:
        logger.warn('Failed to build %s: %s' % (url, e))
        #todo only let errors pass which are authorization errors
        #we do this to allow to pull repo's where potentially user has no access too, so it silently passes
        #this allows us to create this script to also build eg. openvcloud docs even if user has no access

#@todo now use the tools as installed in the gitbook docker

#build all docs with right names as used in 
#https://box.greenitglobe.com/apps/files/?dir=%2FProjects%2Fsberbank%2FSberbankShare%2FDocumentation
#everything which is specified there needs to be build (when md format !)
#when generated docs e.g. out or raml do that generation in this script too, so it really starts from the source code of all our components



