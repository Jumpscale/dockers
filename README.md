> Work In Progress

# Dockers
Project contains all the `Dockerfile`s and `Makefile`s needed to build a preinstalled jumpscale ubuntu images that
has ssh and the needed essential services.

# How To Use
- Clone the repo locally, or where you need to build the images
- Initialize the `submodules`
```bash
cd dockers
git submoudle init
```
- Build your desired image by `cd <image>` the make
```base
cd ./images/ubuntu10.04
make
```
