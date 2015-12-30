from JumpScale import j

class DockerBuilder():
    def __init__(self):
        self.homepath=j.sal.fs.getcwd()
        self.logpath=self.homepath+"/build.log"
        self.errpath=self.homepath+"/errorlast.txt"
        #j.do.delete(self.logpath)
        j.do.delete(self.errpath)
        self.todo=[]
        self.push=True
        self.debug=False
        self._load()

    def _load(self):
        items=j.sal.fs.listDirsInDir(self.homepath,False,True)
        items.sort()
        for item in items:
            if item in ["scripts"]:
                continue
            if item.startswith("_"):
                continue
            if item.find("_")!=-1:
                name=item.split("_",1)[1].strip().lower()
                path=j.sal.fs.joinPaths(self.homepath,item)
                self.todo.append( DockerBuild(self,name,path))


    def ask(self):
        self.todo=j.tools.console.askChoiceMultiple(self.todo, descr="Please select dockers you want to build & push.", sort=False) #do not sort
        self.build()

    def build(self):
        for docker in self.todo:
            docker.build()        


class DockerBuild():

    def __init__(self,builder,name,path):
        self.builder=builder
        self.name=name
        self.path=path
        self._pathPythonBuild=self.path+"/build.py"
        


    def log(self,msg):
        ttime=j.data.time.getLocalTimeHR()
        msg="%-20s %-20s %s\n"%(ttime,self.name,msg)
        print (msg)
        j.sal.fs.writeFile(filename=self.builder.logpath,contents=msg,append=True)

    def build(self):
        pythonbuild=False
        if j.sal.fs.exists(path=self._pathPythonBuild):
            pythonbuild=True
            self.log("Python Build")
            C=j.do.readFile(self._pathPythonBuild)
            curdir=self.path
            rc=0
            out=""
            locals_={"curdir":curdir}
            try:
                # cmd="cd %s;python build.py %s"%(self.path, self.name)
                res=exec(C,globals(),locals_)
            except Exception as e:   
                print(e.with_traceback(e.__traceback__))
                rc=1
          
        else:
            self.log("std docker build")
            cmd="cd %s;docker build -t jumpscale/%s ."%(self.path,self.name)
            if self.builder.debug:
                rc=j.do.executeInteractive(cmd)
            else:
                rc,out=j.do.execute(cmd,dieOnNonZeroExitCode=False)

        if rc>0:
            j.sal.fs.writeFile(filename=self.builder.errpath,contents=out)
            self.log("BUILD IN ERROR")
            raise RuntimeError("could not build")
        else:
            self.log("build ok")

        if pythonbuild:
            d=locals_["d"]
            #d=docker object done in build.py script
            #commit now
            name="jumpscale/%s"%self.name
            self.log("COMMIT:%s"%name)
            d.commit(name)

        if self.builder.push:
            self.push()


    def push(self):
        cmd="docker push jumpscale/%s"%self.name
        rc,out=j.do.execute(cmd,dieOnNonZeroExitCode=False)
        if rc>0:
            self.log("push")
            j.sal.fs.writeFile(filename=self.builder.errpath,contents=out)
            self.log("coud not push (ERROR)")
            raise RuntimeError("could not push")
        else:
            self.log("push ok")

    def __str__(self):
        return self.name

    __repr__=__str__



b=DockerBuilder()
b.push=False
b.debug=True
b.ask()


