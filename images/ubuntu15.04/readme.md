# Ubuntu 15.04
To build the jumpscale/ubuntu:15.04 image just do
```bash
make
```

This image contains the following:
- Working sshd (root password: `js007`)
- Working jumpscale7 installation
- jumpscale ays redis package pre installed
- mc, git, python2.7, curl, wget and tmux are pre-installed
- image auto starts `@ys` on start

#### Original specs
- create docker file to
- install ubuntu 15.04
- make sure ssh is installed
- preinstall ssh key as mentioned in home page of this repo
- std login/passwd root/js007 works over ssh
- install mc / git /python 2.7 / curl / wget
- do update/upgrade
- make sure tmux works & can be used to remote execute something
- install newest jumpscale 7.1
- make sure systen redis is installed & runs in tmux

there are example images to start from which allow tmux & ssh

- write example bash script how to do this (build image & use by means of jsdocker)

