import threading
import time

class Distributor(threading.Thread):
    def __init__(self):
        super(Distributor, self).__init__()
        self.isAlive = False

    def run(self):
        while not self.isAlive:
            time.sleep(1)
            print "i'm here"

    def stop(self):
        self.isAlive= True
