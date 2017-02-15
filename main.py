import os
import time
import threading
import signal
import logging
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options

from routers import router

'''
To solve below issue need to modify ioloop.py of tornado:
Traceback (most recent call last):
  File "main.py", line 42, in <module>
    main()
  File "main.py", line 39, in main
    tornado.ioloop.IOLoop.instance().sta/rt()
  File "C:\Python27\lib\site-packages\tornado\ioloop.py", line 862, in start
    event_pairs = self._impl.poll(poll_timeout)
  File "C:\Python27\lib\site-packages\tornado\platform\select.py", line 63, in poll
    self.read_fds, self.write_fds, self.error_fds, timeout)
select.error: (10038, '')

#In tornado/ioloop.py line 720,set self._timeouts = []
#self._timeouts = None
self._timeouts = [] #
'''
define("port", default=8080, help="Run on the given port", type = int)
is_close = False

def signal_handler(signum, frame):
    global is_close
    logging.info("exiting...")
    is_close = True

def exit():
    global is_close
    if is_close:
        tornado.ioloop.IOLoop.instance().stop()
        logging.info("exit success")

def main():
    #args = sys.argv
    #args.append("--log_file_prefix=/opt/logs/my_app.log")
    #tornado.options.parse_command_line(args)
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    settings = {
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    }
    app = tornado.web.Application(router.handlers,**settings)
    app.listen(options.port)
    print "Listening on port:", options.port
    tornado.ioloop.PeriodicCallback(exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
