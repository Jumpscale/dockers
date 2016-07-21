## Goal
goal is have a docker running which connects to local storx (docker 90_...)
start from ubuntu 1604
mount /storage/builder/sandbox_ub1604/js8/ in ubuntu in /builder

copy required golang files in local docker to start G8OS FS 
from /storage/builder/sandbox_ub1604/js8/jumpscale8

copy the metadata from 
/storage/builder/sandbox_ub1604/js8/md
metada required for G8OS FS

now use the local deployed storx

a minimal docker with all inside to serve required files as needed

## Limitations
Since the g8os fs uses fuse, this usually won't work from inside a docker unless
the docker is running in privileged mode. Also the `fuse` modules must be installed
on the host itself and loaded in the kernel.