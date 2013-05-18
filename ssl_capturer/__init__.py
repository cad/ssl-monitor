import sys
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp

from capturer import SSLV_MulticastProtocol
from transmitter import Push
import transmitter
from pcap import Replayer
print sys.argv
V_H = "224.5.23.2"
V_P = 10020
A_H = "212.175.35.222"
A_P = 443


class CapturingService(object):
    """"""
    
    def __init__(self, multicast_host, multicast_port, monitor_host, monitor_port):
        self.multicast_host = multicast_host
        self.multicast_port = multicast_port
        self.monitor_host = monitor_host
        self.monitor_port = monitor_port
        self.field_id = 'field-1'
        self.monitor_protocol = None
        
    def __multicast_handler(self, datagram, address):
        self.monitor_protocol.callRemote(Push, field_id=self.field_id, frame=datagram)



    def __transmitter_connected(self, protocol):
        print "transmitter connected"
        self.monitor_protocol = protocol


    def ready(self):
        self.transmitter = ClientCreator(reactor, amp.AMP).connectTCP(
            self.monitor_host, self.monitor_port).addCallback(self.__transmitter_connected).addErrback(transmitter.error)

        self.multicast_protocol = SSLV_MulticastProtocol(self.multicast_host, self.__multicast_handler)
        # wheter we are replaying from pcap or not
        if len(sys.argv) > 1:
            if sys.argv[1] == 'pcap':
                print 'Switching to replay mode'
                pcap = sys.argv[2]
                replayer = Replayer(pcap)
                replayer.replay_packets(self.__multicast_handler)
                
        else:
            reactor.listenMulticast(self.multicast_port, self.multicast_protocol, listenMultiple=True)
        print "ready"


    def run(self):
        reactor.run()


if __name__ == '__main__':
    service = CapturingService(V_H, V_P, A_H, A_P)
    service.ready()
    service.run()
    print "Capturing Started"
