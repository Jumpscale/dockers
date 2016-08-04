All the containers in this directory requires a working stor instance
 (docker x86_64/90_ubuntu1604_hoststor)
 
- 01_alpine_fuse installs the fuse filesystem binaries and configuration
  to the alpine base image
- 02_alpine_controller mounts the fuse filesystem, and then starts both redis 
  and the controller
- 03_alpine_core mounts the fuse filesystem, and then starts the core, the core
  is configured to reach over to the controller over the expose controller ports
  

 