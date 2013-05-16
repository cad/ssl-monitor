from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp

from capturer import SSLV_MulticastProtocol
from transmitter import Transmitter



V_H = "224.5.23.2"
V_P = 10020
A_H = "127.0.0.1"
A_P = 9999


class CapturingService(object):
    """"""
    
    def __init__(self, multicast_host, multicast_port, monitor_host, monitor_port):
        self.multicast_host = multicast_host
        self.multicast_port = multicast_port
        self.monitor_host = monitor_host
        self.monitor_port = monitor_port
        
        
    def __multicast_handler(self, datagram, address):
        print datagram        
        self.monitor_protocol.transport.write(datagram)


    def __transmitter_connected(self, protocol):
        print "transmitter connected"
        self.monitor_protocol = protocol


    def ready(self):
        self.transmitter = ClientCreator(reactor, Transmitter).connectTCP(self.monitor_host, self.monitor_port).addCallback(self.__transmitter_connected)
        self.multicast_protocol = SSLV_MulticastProtocol(self.multicast_host, self.__multicast_handler)
        
        
        reactor.listenMulticast(self.multicast_port, self.multicast_protocol, listenMultiple=True)
        print "ready"


    def run(self):
        reactor.run()


if __name__ == '__main__':
    service = CapturingService(V_H, V_P, A_H, A_P)
    print 1
    service.ready()
    print 2
    service.run()
    print 3
