import sys
import logging

from twisted.python import log
from tornado.platform.twisted import TwistedIOLoop
import tornado.httpserver

from twisted.internet import reactor
TwistedIOLoop().install()

from monitor import AMP_SSLMonitorFactory
from websockets import application



def set_up_logging(logger_name):
    logger = logging.getLogger(logger_name)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)


if __name__ == '__main__':
    print "Monitor is started.."
    observer = log.PythonLoggingObserver()
    observer.start()
    set_up_logging('tornado.application')
    set_up_logging('tornado.access')
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    
    reactor.listenTCP(9999, AMP_SSLMonitorFactory())
    reactor.run()
