import os, time, re
from threading import Thread

from script import Script
from serialManager import SerialManager
from common import toBool, strExtract, endline, timeout
from globalvars import client

basePath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "static/json")
testscriptFile = "testscript.json"
instrumentFile = "instrument.json"
settingFile = "setting.json"

def formatData(msg, cmd=""):
    # Add catalog for front end to reconize
    data = {"msg":msg, "cmd":cmd, "catalog":"websocket"}
    return data

REPORT = "report"
SHELL = "shell"
PASS = "pass"

class Distributor():
    def __init__(self):
        self.thread = Thread(target = self.run)
        self.isActive = False
        self.loadScript()
        #self.script = Script(basePath, testscriptFile, instrumentFile, settingFile)
        catalog = self.script.setting.get("device").get("catalog")
        self.serialManager = SerialManager(catalog)
        self.uninitInstruments = {}
        self.initInstruments = {}

        self.initVariables()
    def loadScript(self):
        self.script = Script(basePath, testscriptFile, instrumentFile, settingFile)

    def initVariables(self):
        self.isTestStart = False
        self.isWrite = True
        # "start" is the entrance of testscript
        self.startScriptId = "start"
        self.nextScriptId = "start"

        self.dynamicVars = {}

        self.responseBuffer = ""

        self.repeatTimes = {}

    def start(self):
        self.isActive = True
        self.thread.start()

    def stop(self):
        self.isActive = False
        self.thread.join()

    def startTest(self):
        self.isTestStart = True

    def stopTest(self):
        self.initVariables()

    def callAfter(self, func , *args):
        return func(*args)

    def initSerial(self):
        self.serialManager.listSerial()
        for instrument in self.script.instrument:
            item =  instrument.keys()[0]
            infor = instrument.get(item).get("information")
            setting = instrument.get(item).get("serial")
            device_id = {"vendor_id":setting.get("vendor_id"),"model_id":setting.get("model_id")}
            if toBool(infor.get("usage")) == True:
                try:
                    index = self.serialManager.devices.values().index(device_id)
                except ValueError:
                    self.uninitInstruments[item] = instrument.get(item)
                else:
                    self.initInstruments[item] = instrument.get(item)
                    setting["port"] = self.serialManager.devices.keys()[index]
                    self.serialManager.openSerial(setting)

    def run(self):
        while self.isActive == True:
            if self.isTestStart == True:
                self.runScript()
                time.sleep(0.01)
            else:
                #print "i'm executor running"
                time.sleep(0.5)

    def runScript(self):
        scriptId = self.nextScriptId
        if  self.delayScript(scriptId) == True:
            return
        if scriptId == "none":
            print "the dynamic vars are: ",self.dynamicVars
            self.stopTest()
            return

        isCommandFinish, isResponseMatch, data, isTimeout = self.runCommand(scriptId)
        if isCommandFinish == True:
            # Enable write after read the response or timeout
            self.isWrite = True
            if self.responseVariable == "":
                data = PASS
            else:
                self.dynamicVars[self.responseVariable] = data

            # Get delay start time
            self.delayStart = time.time()
            commandTime = round((time.time()-self.commandStart),3)
            print isResponseMatch, data, commandTime

            isInSpec, data = self.checkSpec(isResponseMatch, data, self.execString, self.spec)

            self.nextScriptId = self.nextScript(scriptId, isInSpec)
            print self.nextScriptId, isInSpec, data
            self.report(isInSpec, commandTime, data)

    def report(self, result, commandTime, data):
            report = {}
            report["groupId"] = self.groupId
            report["groupNameCh"] = self.groupNameCh
            report["groupNameEn"] = self.groupNameEn
            report["commandNameCh"] = self.commandNameCh
            report["commandNameEn"] = self.commandNameEn
            report["spec"] = self.spec
            report["unit"] = self.unit

            report["result"] = result
            report["commandTime"] = commandTime
            report["data"] = data
            setting = self.script.setting.get("report")
            msg = {"setting":setting,"data":report}

            client.broadcast(formatData(msg, REPORT))

    def nextScript(self, scriptId ,isInSpec):
        if isInSpec == True:
            nextScriptId = self.passAction
        else:
            if self.repeatTimes.has_key(scriptId):
                self.repeatTimes[scriptId] += 1
            else:
                self.repeatTimes[scriptId] = 1
            if self.repeatTimes[scriptId] > self.repeatTime:
                nextScriptId = self.endAction
            else:
                nextScriptId = self.failAction

        return nextScriptId

    def runCommand(self, scriptId):
        # Write command
        if self.isWrite == True:
            # Disable write for read
            self.isWrite = False
            # Get script information
            self.getScriptInfor(scriptId)
            self.writeCommand(self.command, self.visaName)
            # Get command start time
            self.commandStart = time.time()
            # Clean read buffer
            self.responseBuffer = ""

            # strip endline
            client.broadcast(formatData(self.command.strip(), SHELL))

        # Read response
        response = self.readResponse(self.visaName)
        if response != "":
            client.broadcast(formatData(response.strip(), SHELL))
        # Keep response in buffer
        self.responseBuffer += response
        isMatch, data, isException = self.matchResponse(self.responseBuffer, response)
        isTimeout = timeout(self.commandTimeout, self.commandStart)
        if isMatch == True or isTimeout == True or isException == True:
            isCommandFinish = True
        else:
            isCommandFinish = False

        return isCommandFinish, isMatch, data, isTimeout

    def delayScript(self, scriptId):
        if self.isWrite == True:
            if scriptId != self.startScriptId :
                if timeout(self.commandDelay, self.delayStart) != True :  #if in delay time , nothing to do . don't delay at the first beginning
                    return True
        return False

    def writeCommand(self, command, visaName):
        command = command.encode("ascii")
        if command == "":
            return
        if visaName == "telnet":
            pass
        elif visaName == "server":
            pass
        elif visaName == "telnetcon":
            pass
        elif visaName == "shell":
            pass
        elif visaName == "dnct":
            pass
        elif visaName == "dnctcon":
            pass
        else:
            if self.serialManager.initSerials.has_key(visaName):
                self.serialManager.initSerials.get(visaName).writeSerial(command)

    def readResponse(self, visaName):
        response = ""
        if visaName == "telent":
            pass
        elif visaName == "sever":
            pass
        elif visaName == "dnct" or visaName == "dnctcon":
            pass
        elif visaName == "shell":
            pass
        else:
            if self.serialManager.initSerials.has_key(visaName):
                response = self.serialManager.initSerials.get(visaName).readSerial()

        return response

    def matchResponse(self, responseBuffer, response):
        isMatch = False
        data = ""
        isException = False

        reReg = re.escape(self.exception)
        finds = re.findall(reReg, responseBuffer)
        if len(finds) >= 1:
            isException = True
            return isMatch, data, isException
        if response == "":
            #reReg = re.escape(self.response)
            reReg = self.response
            finds = re.findall(reReg, responseBuffer)
            if len(finds) >= 1:
                isMatch = True
                data = finds[0]
        else:
            time.sleep(0.05)

        return isMatch, data, isException

    def checkSpec(self, isResponseMatch, data, execString, spec):
        result = False
        # ExecString should overwrite value of result, if there's spec checking in execString
        try:
            exec(execString)
        except:
            pass
        else:
            pass

        print "the result is :",result
        if isResponseMatch != True:
            isInSpec = False
        else:
            if spec.lower() == PASS:
                isInSpec = True
                print "the isInSpec is: ",isInSpec
            else:
                reReg = spec
                finds = re.findall(reReg, data)
                if len(finds) >= 1:
                    isInSpec = True
                else:
                    isInSpec = False
                print "i'm surpprised"
        # Merge spec check result of execString and re
        isInSpec = result or isInSpec
        return  isInSpec, data

    def getScriptInfor(self, scriptId):
        # Get original string data from script
        testscript = self.script.testscript.get(scriptId)
        self.groupId = testscript.get("group_id")
        self.groupNameCh = testscript.get("group_name_ch")
        self.groupNameEn = testscript.get("group_name_en")
        self.commandNameCh = testscript.get("name_ch")
        self.commandNameEn = testscript.get("name_en")
        suffix = endline(testscript.get("suffix"))
        self.command = self.formatCommand(testscript.get("command")+suffix)
        self.response = self.formatResponse(testscript.get("response"))
        self.responseVariable = testscript.get("variable")
        self.exception = self.formatException(testscript.get("exception"))
        self.execString = testscript.get("exec")
        self.spec = self.formatSpec(testscript.get("spec"))
        self.unit = testscript.get("unit")
        self.commandTimeout = int(testscript.get("timeout"))/1000
        self.commandDelay = int(testscript.get("delay"))/1000
        visa = testscript.get("visa")
        self.visaName = self.initInstruments.get(visa).get("serial").get("port")

        self.passAction = testscript.get("pass")
        self.failAction = testscript.get("fail")
        self.endAction = testscript.get("end")
        self.isReport = toBool(testscript.get("report"))
        self.isDatabase = toBool(testscript.get("database"))
        self.repeatTime = int(testscript.get("repeat"))


    def formatCommand(self, commandStr):
        isExtract, prefix, extract, suffix = strExtract(commandStr)
        if isExtract == True:
            # variable name is extract
            if self.dynamicVars.has_key(extract):
                command = prefix + self.dynamicVars.get(extract) + suffix
        else:
            command = commandStr

        return command

    def formatResponse(self, responseStr):
        isExtract, prefix, extract, suffix = strExtract(responseStr)
        if isExtract == True:
            # variable name is extract
            if self.dynamicVars.has_key(extract):
                response = prefix + self.dynamicVars.get(extract) + suffix
        else:
            response = responseStr

        return response

    def formatException(self, exceptionStr):
        return exceptionStr

    def formatSpec(self, specStr):
        isExtract, prefix, extract, suffix = strExtract(specStr)
        if isExtract == True:
            # variable name is extract
            if self.dynamicVars.has_key(extract):
                spec = prefix + self.dynamicVars.get(extract) + suffix
        else:
            spec = specStr

        return spec

if __name__ == "__main__":
    d = Distributor()
    d.initSerial()
    print d.serialManager.initSerials
    #print d.initInstruments
    d.start()
    d.startTest()
