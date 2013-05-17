from twisted.internet import reactor

from monitor import AMP_SSLMonitorFactory




if __name__ == '__main__':
    print "Monitor is started.."
    reactor.listenTCP(9999, AMP_SSLMonitorFactory())
    reactor.run()
