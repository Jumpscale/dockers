> Work In Progress

# Dockers
Project contains all the `Dockerfile`s and `Makefile`s needed to build a preinstalled jumpscale ubuntu images that
has ssh and the needed essential services.

# How To Use
1 - Clone the repo locally, or where you need to build the images
2 - Initialize the `submodules`
```bash
cd dockers
git submoudle init
```
3- Build your desired image by `cd <image>` the make
```base
cd ./ubuntu10.04
make
```
