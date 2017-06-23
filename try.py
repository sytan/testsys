# encoding: UTF-8
from Queue import Queue, Empty
from threading import Thread

class EventManager:
    #----------------------------------------------------------------------
    def __init__(self):
        self.eventQueue = Queue()
        self.isActive = False
        self.thread = Thread(target = self.run)

    #----------------------------------------------------------------------
    def run(self):
        while self.isActive == True:
            try:
                event = self.eventQueue.get(block = True, timeout = 1)
                self.eventProcess(event)
            except Empty:
                pass

    #----------------------------------------------------------------------
    def eventProcess(self, event):
        event.handler(*event.args)

    #----------------------------------------------------------------------
    def start(self):
        self.isActive = True
        self.thread.start()

    #----------------------------------------------------------------------
    def stop(self):
        self.isActive = False
        self.thread.join()

    #----------------------------------------------------------------------
    def addEvent(self, event):
        self.eventQueue.put(event)

"""class Event"""
class Event():
    def __init__(self, handler = None, args = None):
        self.handler = handler
        self.args = args
