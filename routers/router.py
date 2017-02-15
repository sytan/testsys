from handlers import handler

handlers = [
    ("/", handler.IndexHandler),
    ("/ws", handler.WebSocketHandler),
    ("/book/page",handler.PageHandler),
]
