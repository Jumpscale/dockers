from JumpScale import j

import click


class DockerBuilder():

    def __init__(self):
        self.homepath = j.sal.fs.getcwd()
        self.logpath = self.homepath + "/build.log"
        self.errpath = self.homepath + "/errorlast.txt"
        # j.sal.fs.remove(self.logpath)
        j.sal.fs.remove(self.errpath)
        self.todo = []
        self.push = True
        self.debug = False
        self._load()

    def _load(self):
        items = j.sal.fs.listDirsInDir(self.homepath, False, True)
        items.sort()
        for item in items:
            if item in ["scripts"]:
                continue
            if item.startswith("_"):
                continue
            if item.find("_") != -1:
                name = item.split("_", 1)[1].strip().lower()
                path = j.sal.fs.joinPaths(self.homepath, item)
                self.todo.append(DockerBuild(self, name, path))

    def setDockerHost(self, host):
        host, port = host.split(':')
        j.sal.docker.connectRemoteTCP(host, port)

    def ask(self):
        self.todo = j.tools.console.askChoiceMultiple(self.todo, descr="Please select dockers you want to build & push.", sort=False)  # do not sort
        self.build()

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
            self.log("Python Build")
            C = j.sal.fs.fileGetContents(self._pathPythonBuild)
            curdir = self.path
            out = ""
            locals_ = {"curdir": curdir}
            try:
                res = exec(C, globals(), locals_)
            except Exception as e:
                print(e.with_traceback(e.__traceback__))
                rc = 1

        else:
            self.log("std docker build")
            imageName = 'jumpscale/%s' % self.name
            try:
                output = j.sal.docker.build(self.path, imageName, output=True)
                self.log("build ok")
            except:
                j.sal.fs.writeFile(filename=self.builder.errpath, contents=output)
                self.log("BUILD IN ERROR")
                rc = 1
                raise RuntimeError("could not build")

        if pythonbuild and rc == 0:
            d = locals_["d"]
            # d=docker object done in build.py script
            # commit now
            name = "jumpscale/%s" % self.name
            self.log("COMMIT:%s" % name)
            d.commit(name, delete=True, force=True)

        if self.builder.push and rc == 0:
            self.push()

    def push(self):
        try:
            image = 'jumpscale/%s' % self.name
            output = j.sal.docker.push(image, output=True)

            self.log("push ok")
        except:
            j.sal.fs.writeFile(filename=self.builder.errpath, contents=output)
            self.log("coud not push (ERROR)")
            raise RuntimeError("could not push")

    def __str__(self):
        return self.name

    __repr__ = __str__


@click.command()
@click.option('--host', default=None, help='address:port of the docker host to use')
@click.option('--debug/--nodebug', default=True, help='enable or disable debug (default: True)')
@click.option('--push/--nopush', default=False, help='push images to docker hub afrer building (default:False)')
def build(host, debug, push):
    builder = DockerBuilder()
    builder.push = push
    builder.debug = debug
    if host:
        builder.setDockerHost(host)
    builder.ask()

if __name__ == '__main__':
    build()
