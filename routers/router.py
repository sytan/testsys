from handlers import handler

handlers = [
    ("/", handler.IndexHandler),
    ("/ws", handler.WebSocketHandler),
    ("/testdetail",handler.testdetailHandler),
]
