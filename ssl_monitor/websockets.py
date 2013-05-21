import os
import imp
import argparse
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import tornado.escape
from tornado.platform.twisted import TwistedIOLoop
import json
import datetime


sockets = {}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html", title="SSL-MONITOR | Game Viewer")


class GameHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        self.field_name = None
        super(GameHandler, self).__init__(*args, **kwargs)


    def open(self):
        self.field_name = self.get_argument("fieldname", None, True)
        #print self.field_name
        field_socket = sockets.get(self.field_name, None)
        if not field_socket:
            sockets[self.field_name] = [self,]
        else:
            sockets[self.field_name].append(self)
        print "WebSocket opened"  
    
            
    def on_message(self, msg):
        print "WebSocket message", msg
        
    def on_close(self):
        sockets[self.field_name].remove(self)
        print "Websocket closed"



application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/track', GameHandler),
])

if __name__ == '__main__':
    
    print '[switchboard] Swtichboard is runing at 0.0.0.0:8888\nQuit with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
