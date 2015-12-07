from JumpScale import j

class DockerBuilder():
    def __init__(self):
        self.homepath=j.sal.fs.getcwd()
        self.logpath=self.homepath+"/build.log"
        self.errpath=self.homepath+"/errorlast.txt"
        j.do.delete(self.logpath)
        j.do.delete(self.errpath)

        self._load()
        self.todo=[]

        self.push=True        

    def _load(self):
        items=j.sal.fs.listDirsInDir(self.homepath,False,True)
        items.sort()
        for item in items:
            if item in ["scripts"]:
                continue
            if item.startswith("_"):
                continue
            name=item.split("_",1)[1].strip().lower()
            path=j.sal.fs.joinPaths(homepath,item)
           self.todo += DockerBuild(self,name,path)


    def ask(self):
        self.todo=j.console.askChoiceMultiple(self.todo, descr="Please select dockers you want to build & push.", sort=False) #do not sort
        self.build()

    def build(self):
        for docker in self.todo:
            docker.build())        



class DockerBuild():

    def __init__(self,builder,name,path):
        self.builder=builder
        self.name=name
        self.path=path
        self._pathPythonBuild=self.path+"/build.py"


    def log(self,msg):
        msg="%-20s %s\n"%(self.name,msg)
        j.sal.fs.writeFile(filename=self.builder.logpath,contents=msg,append=True)

    def build(self):
        if j.sal.fs.exists(path=self._pathPythonBuild):
            self.log("Python Build")
            cmd="cd %s;python build.py %s"%self.name
        else:
            self.log("std docker build")
            cmd="cd %s;docker build -t jumpscale/%s ."%self.name
        rc,out=j.do.execute(cmd,die=False)
        if rc>0:
            j.sal.fs.writeFile(filename=self.builder.errpath,contents=out)
            self.log("BUILD IN ERROR")
        else:
            self.log("build ok")
        if self.builder.push:
            self.push()


    def push(self):
        cmd="docker push %s"%self.name
        rc,out=j.do.execute(cmd,die=False)
        if rc>0:
            self.log("push")
            j.sal.fs.writeFile(filename=self.builder.errpath,contents=out)
            self.log("coud not push (ERROR)")
        else:
            self.log("push ok")

    def __str__(self):
        return self.name

    __repr__=__str__



b=DockerBuilder()
b.ask()


