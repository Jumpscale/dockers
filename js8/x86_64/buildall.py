#!/usr/local/bin/jspython

from JumpScale import j

import click


class DockerBuilder():

    def __init__(self):
        self.homepath = j.sal.fs.getcwd()
        self.logpath = self.homepath + "/build.log"
        self.errpath = self.homepath + "/errorlast.txt"
        j.sal.fs.remove(self.errpath)
        self.todo = []
        self.push = True
        self.debug = False
        self._load()

    def _load(self):
        items = sorted(j.sal.fs.listDirsInDir(self.homepath, False, True))
        for item in items:
            if item in ["scripts"]:
                continue
            if item.startswith("_"):
                continue
            if item.find("_") != -1:
                name = item.split("_", 1)[1].strip().lower()
                path = j.sal.fs.joinPaths(self.homepath, item)
                self.todo.append(DockerBuild(self, name, path))

    def ask(self):
        self.todo = j.tools.console.askChoiceMultiple(self.todo, descr="Please select dockers you want to build & push.", sort=False)  # do not sort

    def build(self):
        for docker in self.todo:
            docker.build()


class DockerBuild():

    def __init__(self, builder, name, path):
        self.builder = builder
        self.name = name
        self.path = path
        self._pathPythonBuild = self.path + "/build.py"

    def log(self, msg):
        ttime = j.data.time.getLocalTimeHR()
        msg = "%-20s %-20s %s\n" % (ttime, self.name, msg)
        print(msg)
        j.sal.fs.writeFile(filename=self.builder.logpath, contents=msg, append=True)

    def build(self):
        pythonbuild = False
        rc = 0
        if j.sal.fs.exists(path=self._pathPythonBuild):
            pythonbuild = True

            self.log("Python Build:%s"%self._pathPythonBuild)
            # C = j.sal.fs.fileGetContents(self._pathPythonBuild)

            command="cd %s;python3 build.py"%(self.path)
            rc=j.do.executeInteractive(command)
            if rc>0:                
                raise j.exceptions.RuntimeError("could not build %s"%self.name)
            
        else:
            self.log("std docker build:%s" % self.path)
            imageName = 'jumpscale/%s' % self.name
            output = j.sal.docker.build(self.path, imageName, output=True, force=True)
            self.log("build ok")

            if not "Successfully built" in output:
                from IPython import embed
                print ("DEBUG NOW sdsd")
                embed()
                p
                
                raise j.exceptions.RuntimeError("Cannot build %s from dockerfile"%self.name)

        if self.builder.push:
            nopushfile=j.sal.fs.joinPaths(self.path,".nopush")
            if j.sal.fs.exists(nopushfile):
                return
            self.push()

    def push(self):
        try:
            image = 'jumpscale/%s' % self.name
            output = j.sal.docker.push(image, output=True)
            self.log("push ok")
        except Exception as e:
            j.sal.fs.writeFile(filename=self.builder.errpath, contents=str(e))
            self.log("coud not push (ERROR)")
            raise j.exceptions.RuntimeError("could not push.\n%s" % e)


    def __str__(self):
        return self.name

    __repr__ = __str__


@click.command()
@click.option('--host', '-h', default=None, help='address:port of the docker host to use')
@click.option('--debug/--nodebug', default=True, help='enable or disable debug (default: True)')
@click.option('--push/--nopush', default=False, help='push images to docker hub afrer building (default:False)')
@click.option('--image', '-i', default="", help='specify which image to build e.g. 2_ubuntu1604, if not specified then will ask, if * then all.')
def build(host, debug, push, image=""):
    """
    builds dockers with jumpscale components
    if not options given will ask interactively

    to use it remotely, docker & jumpscale needs to be pre-installed

    """
    builder = DockerBuilder()
    builder.push = push
    builder.debug = debug
    if host:
        c = j.tools.cuisine.get(host)
        c.executor.sshclient.rsync_up(j.sal.fs.getcwd(), "/tmp/dockerbuild/")
        cmd = "cd /tmp/dockerbuild/;python3 buildall.py"
        if push:
            cmd += " --push"
        if image == "":
            builder.ask()
            image = builder.todo[0].name

        cmd += " -i %s" % image

        c.core.run(cmd)
        return

    if image == "":
        builder.ask()
    elif image == "*":
        pass
    else:
        builder.todo = [item for item in builder.todo if item.name == image]
        if builder.todo == []:
            raise j.exceptions.Input("cannot find specified image:%s" % image)

    builder.build()


if __name__ == '__main__':
    build()
