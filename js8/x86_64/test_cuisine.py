#!/usr/local/bin/jspython

from JumpScale import j

# c=j.tools.cuisine.get("10.10.69.46")
c=j.tools.cuisine.get("ovh4")

from IPython import embed
print ("DEBUG NOW sdsd")
embed()

p

S="""
ls /
echo "done"
"""
print(c.core.run_script(S))



