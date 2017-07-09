from serial import Serial
import subprocess
import glob
import re

from common import toBool, toNone

class MySerial(Serial):
    def __init__(self):
        Serial.__init__(self)

    def openSerial(self):
        if self.isOpen() == False:
            self.open()

    def readSerial(self):
        readBuffer = ""
        size = self.inWaiting()
        if size >= 1:
            readBuffer = self.read(size)
        return readBuffer

    def writeSerial(self, cmd):
        if cmd != "":
            self.write(cmd)
        return len(cmd)

    def flushSerial(self):
        self.flushInput()

    def closeSerial(self):
        self.close()

class SerialManager():
    def __init__(self, catalog=None):
        self.devices = {}
        self.initSerials = {}
        self.catalog = catalog
        if catalog == None:
            self.catalog = ["/dev/ttyACM*","/dev/ttyUSB*"]

    def listSerial(self):
        deviceNames = []
        for tty in self.catalog:
            dev = glob.glob(tty)
            deviceNames += dev
        for dev in deviceNames:
            cmd = "udevadm info "+ dev
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            p.wait()
            info = p.stdout.read()
            vendor_id =  re.search(r"ID_VENDOR_ID=(.+)",info).group(1)
            model_id =  re.search(r"ID_MODEL_ID=(.+)",info).group(1)
            self.devices[dev]={"vendor_id":vendor_id,"model_id":model_id}

    def openSerial(self, setting):
        ser = MySerial()
        ser.port = setting.get('port')
        ser.baudrate = int(setting.get('baudrate'))     #type transfer from str to int
        ser.bytesize = int(setting.get('bytesize'))
        ser.parity = setting.get('parity')
        ser.stopbits = int(setting.get('stopbits'))
        ser.timeout = int(setting.get('timeout'))
        ser.xonxoff = toBool(setting.get('xonxoff'))      #type transfer from str to bool
        ser.rtscts = toBool(setting.get('rtscts'))
        ser.dsrdtr = toBool(setting.get('dsrdtr'))
        ser.writeTimeout = toNone(setting.get('writetimeout'))
        ser.interCharTimeout = toNone(setting.get('interchartimeout'))   #type transfer from str to None
        ser.openSerial()
        self.initSerials[ser.port] = ser

    def closeSerial(self, ser):
        if self.initSerials.has_key(ser.port):
            self.initSerials.pop(ser.port)
            ser.closeSerial()

if __name__ == "__main__":
    serialManager = SerialManager()
    serialManager.listSerial()
    print serialManager.devices
    #print type(mySerial.device)
    #print mySerial.device
