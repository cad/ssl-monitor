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
    
    def __init__(self, field_id, multicast_host, multicast_port, monitor_host, monitor_port, mode='live', pcap=None):
        self.multicast_host = multicast_host
        self.multicast_port = multicast_port
        self.monitor_host = monitor_host
        self.monitor_port = monitor_port
        self.field_id = field_id
        self.monitor_protocol = None
        self.mode = mode
        self.pcap_f = pcap

    def __multicast_handler(self, datagram, address):
        self.monitor_protocol.callRemote(Push, field_id=self.field_id, frame=datagram)



    def __transmitter_connected(self, protocol):
        print "transmitter connected"
        self.monitor_protocol = protocol


    def ready(self):
        self.transmitter = ClientCreator(reactor, amp.AMP).connectTCP(
            self.monitor_host, self.monitor_port).addCallback(self.__transmitter_connected).addErrback(transmitter.error)

        
        # wheter we are replaying from pcap or not
        if self.mode == 'pcap':
            print 'Switching to replay mode'
            pcap = self.pcap_f
            replayer = Replayer(pcap)
            replayer.replay_packets(self.__multicast_handler)
                
        else:
            self.multicast_protocol = SSLV_MulticastProtocol(self.multicast_host, self.__multicast_handler)
            reactor.listenMulticast(self.multicast_port, self.multicast_protocol, listenMultiple=True)
        print "ready"


    def run(self):
        reactor.run()
