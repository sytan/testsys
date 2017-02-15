
import tornado.websocket

clients = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print "hello, web"
        self.render('../views/index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        clients.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        if message == "exit":
            signal_handler(None, None)

        print 'tornado received from client: %s' % message
        self.write_message('got it!')

    def on_close(self):
        print 'connection closed'
        clients.remove(self)

class PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello, i'm page")
