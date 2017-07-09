import json

READ = "read"
WRITE = "write"

class Client():
    def __init__(self):
        self.clients = {}

    def add(self, peername, connection, priority = READ):
        self.clients[peername] = {}
        self.clients[peername]["connection"] = connection
        self.clients[peername]["priority"] = priority

    def remove(self, peername):
        if self.clients.has_key(peername):
            self.clients.pop(peername)

    def list(self):
        return self.clients

    def broadcast(self, data):
        for peername in self.clients:
            con = self.clients.get(peername).get("connection")
            con.write_message(data)
