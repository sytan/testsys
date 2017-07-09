#! /usr/bin/env python
#-*- coding: UTF-8 -*-

import tornado.websocket
import json
import re
from models import mydistributor
from globalvars import client

START = "start"
INIT = "init"
RELOAD = "reload"
SHELL = "shell"

def formatData(msg, cmd=""):
    # Add catalog for front end to reconize
    data = {"msg":msg, "cmd":cmd, "catalog":"websocket"}
    return data

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        setting = mydistributor.script.setting.get("report")
        self.render('index.html', reportSetting = setting)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        #clients.append(self)
        print("WebSocket opened")
        peername = self.stream.socket.getpeername()
        peername = peername[0]+":"+str(peername[1])
        client.add(peername, self)
        print client.list()

    def on_message(self, message):
        msg = json.loads(message)
        print msg
        #if message == "exit":
        #    signal_handler(None, None)
        if msg.has_key('msg') and msg.has_key('cmd'):
            print msg['cmd'],msg['msg']
            command = msg['msg']
            if command == START:
                mydistributor.initSerial()
                mydistributor.startTest()
            elif command == INIT:
                pass
                #mydistributor.initSerial()
            elif command == RELOAD:
                mydistributor.loadScript()
            else:
                client.broadcast(formatData(command, SHELL))
                pass

    def on_close(self):
        print 'connection closed'
        peername = self.request.connection.context.address
        #peername = self.stream.socket.getpeername()
        peername = peername[0]+":"+str(peername[1])
        client.remove(peername)
        print client.list()

class testdetailHandler(tornado.web.RequestHandler):
    def get(self):
        setting = mydistributor.script.setting.get("report")
        self.render('testdetail.html', reportSetting = setting)
