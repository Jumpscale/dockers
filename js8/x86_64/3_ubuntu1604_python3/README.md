
# docker image python installed in development mode & all required modules

see docker location on docker hub
- https://hub.docker.com/r/jumpscale/ubuntu1604_python3/

std passwd
- root/gig1234

## use from non jumpscale enabled system

easiest way to use (windows & max)
- install https://www.docker.com/toolbox
- login using your docker account (create one if you don't have yet)
- click create
- look for jumpscale/ubuntu1604_python3

careful the std passwd is now used, use jsdocker for more security (see below)

## use from jumpscale enabled system

```
docker pull jumpscale/ubuntu1604_python3
jsdocker new -n ubuntu1604_python3 -b jumpscale/ubuntu1604_python3 --start
```

you can now login with
```
ssh localhost -p 9022
```
port will change depending nr of dockers on your machine

# to build
make sure jumpscale has been installed on system
```
mkdir -p /opt/code/github/jumpscale
cd /opt/code/github/jumpscale
git clone https://github.com/Jumpscale/dockers.git
cd dockers/js8
js buildall.py
#chose this directory
```


# to push back to the docker hub

we do an autobuild in jumpscale/ubuntu1604_python3 so no real need to do this manually
```
docker login
docker push jumpscale/ubuntu1604_python3
```

# remarks

## runit

this docker uses runit to schedule all processes some useful commands
- more info on http://smarden.org/runit/faq.html

imagine the docker name is 04c9611bd06a
```
#find docker id 04...
docker ps 
#restart ssh
docker exec 04c9611bd06a sv restart sshd
```

## ssh troubles

ssh tries to use all private local keys
it could be your ssh server is configured to not allow too many attempts
to make sure that no ssh keys are used and only try with login/passwd combination do following
```
ssh -o PubkeyAuthentication=no localhost -p 9026
```
port you can find by doing 'docker ps'


