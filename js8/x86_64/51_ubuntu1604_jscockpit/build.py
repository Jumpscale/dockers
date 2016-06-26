from JumpScale import j

def printInfo(msg):
    print (msg)

def update():
    """
    Update the git repo used during installation of the cockpit.
    Run that before doing install to be sure to have last code.
    """
    printInfo("Update required git repository to last version")
    repos = [
        'https://github.com/JumpScale/jscockpit.git'
    ]
    for url in repos:
        j.do.pullGitRepo(url=url, ssh=False)


update()

"""
Build g8cockpit docker image
"""

printInfo("Building g8cockpit image")

j.tools.cuisine.local.core.run("""cd /opt/code/github/JumpScale/jscockpit
    python scripts/building.py --nopush""")
