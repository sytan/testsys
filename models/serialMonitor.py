from pyudev import Context, Monitor, MonitorObserver
from callBack import callAfter, Event

class SerialMonitor():
    def __init__(self, deviceFilter):
        self.deviceFilter = deviceFilter
        self.device = None
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem='tty', device_type= None)
        self.observer = MonitorObserver(monitor, callback=self.deviceEvent, name='monitor-observer')
        self.observer.daemon = False
        self.addEvent = None
        self.removeEvent = None

    def deviceEvent(self,device):
        self.device = device
        if device.action == "add":
            deviceId = {'vendorId':device['ID_VENDOR_ID'], 'modelId':device['ID_MODEL_ID']}
            if deviceId in self.deviceFilter:
                #print device['DEVNAME']," was detected\n"
                if self.addEvent != None :
                    tempEvent = Event()
                    tempEvent.handler = self.addEvent.handler
                    tempEvent.args = (device,) + self.addEvent.args
                    callAfter.addEvent(tempEvent)
        elif device.action == "remove":
            #print device['DEVNAME']," was removed\n",
            if self.removeEvent != None :
                tempEvent = Event()
                tempEvent.handler = self.removeEvent.handler
                tempEvent.args = (device,) + self.removeEvent.args
                callAfter.addEvent(tempEvent)
            #if callable(self.removeCallback.callable) :
            #    self.removeCallback.callable(*self.removeCallback.args)
        else:
            pass
    def onAdd(self, callableObj, *args):
        assert callable(callableObj), "callableObj is not callable"
        self.addEvent = Event(callableObj, *args)
    def onRemove(self, callableObj, *args):
        assert callable(callableObj), "callableObj is not callable"
        self.removeEvent = Event(callableObj, *args)
    def start(self):
        self.observer.start()
    def stop(self):
        self.observer.stop()

if __name__ == '__main__' :
    import time
    callAfter.start()
    #deviceFilter = [{"vendorId":'2341',"modelId":'003e'},{'vendorId':'046d','modelId':'c05a'}]
    deviceFilter = [{"vendorId":'2341',"modelId":'003e'}]
    serMonitor = SerialMonitor(deviceFilter)
    serMonitor.start()
    def handler(device,str1,str2):
        print "the port is ",device['DEVNAME'], str1, str2
    serMonitor.onAdd(handler,"the action is ","add")
    serMonitor.onRemove(handler,"the action is ","remove")
    time.sleep(10)
    serMonitor.stop()
    callAfter.stop()
