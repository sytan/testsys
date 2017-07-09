import json
import os

class Script():
    def __init__(self,basePath, testscript, instrument, setting):
        self.testscriptPath = os.path.join(basePath, testscript)
        self.instrumentPath = os.path.join(basePath,instrument)
        self.settingPath = os.path.join(basePath,setting)

        self.testscript = self.loadFile(self.testscriptPath)
        self.instrument = self.loadFile(self.instrumentPath)
        self.setting = self.loadFile(self.settingPath)

    def loadFile(self,path):
        with open(path) as f:
            return json.load(f)

    def writeFile(self, path, data):
        with open(path, 'w') as  f:
            json.dump(data, f, indent= 2)

if __name__ == "__main__":
    basePath = "../static/json"
    script = Script(basePath,"testscript.json","instrument.json","setting.json")
    print type(script.setting),type(script.instrument),type(script.testscript)
    print script.testscript.get("step_3").get("response")
    print script.testscript.get("step_3").get("suffix")
    script.setting["name"] = "12345"
    script.writeFile(script.settingPath, script.setting)
    reReg = script.testscript.get("step_1").get("response")
    print reReg
    import re
    #reReg = re.escape(reReg)
    #print reReg
    string = "sw:01.32.78"
    finds = re.findall(reReg, string)
    t = re.findall("sw:([0-9\.]{8})",string)
    print finds, t
    e = {"age":28.125,"name":"Lily"}
    s = script.testscript.get("stop").get("exec")
    exec(s)
