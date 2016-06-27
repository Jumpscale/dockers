from JumpScale import j

def printInfo(msg):
    print (msg)

printInfo("Update required git repository to last version")

dest = j.do.pullGitRepo(url='https://github.com/JumpScale/jscockpit.git', ssh=False)

printInfo("Build docker image")

j.tools.cuisine.local.core.run("""cd %s;python scripts/building.py --nopush"""%dest)
