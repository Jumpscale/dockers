Full documentation [here](http://gig.gitbooks.io/jumpscale/content/Howto/How%20To%20Use%20Docker.html)

# Dockers
Project contains all the `Dockerfile`s and `Makefile`s needed to build a preinstalled jumpscale ubuntu images that
has ssh and the needed essential services.

# How To Use
- Clone the repo locally, or where you need to build the images
- Build your desired image by `cd <image>` then make
```base
cd dockers/images/ubuntu10.04
make
```
