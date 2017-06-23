
import tornado.websocket
import json

clients = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        clients.append(self)
        print("WebSocket opened")

    def on_message(self, message):
        msg = json.loads(message)
        #if message == "exit":
        #    signal_handler(None, None)
        if msg.has_key('Msg') and msg.has_key('Cmd'):
            print msg['Cmd'],msg['Msg']
            self.write_message(message)
        #self.write_message('got it!')

    def on_close(self):
        print 'connection closed'
        clients.remove(self)

class PageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello, i'm page")
