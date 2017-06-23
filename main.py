import os
import time
import threading
import signal
import logging
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options


from routers import router
from models import distribute

define("port", default=8080, help="Run on the given port", type = int)
is_close = False

distributor = distribute.Distributor()
distributor.setDaemon(True)

def signal_handler(signum, frame):
    global is_close
    logging.info("exiting...")
    is_close = True

def exit():
    global is_close
    if is_close:
        tornado.ioloop.IOLoop.instance().stop()
        distributor.stop()
        logging.info("exit success")

def main():
    #args = sys.argv
    #args.append("--log_file_prefix=/opt/logs/my_app.log")
    #tornado.options.parse_command_line(args)
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    settings = {
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'template_path': os.path.join(os.path.dirname(__file__),"views"),
    'debug': True, #when in developing
    }
    app = tornado.web.Application(router.handlers, **settings)
    app.listen(options.port)
    print "Listening on port:", options.port

    distributor.start()
    tornado.ioloop.PeriodicCallback(exit, 100).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
