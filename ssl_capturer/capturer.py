from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor



class SSLV_MulticastProtocol(DatagramProtocol):
    
    def __init__(self, multicast_address, packet_handler):
        self.multicast_address = str(multicast_address)
        #self.multicast_port = int(multicast_port)
        self.__packet_handler = packet_handler


    def startProtocol(self):
        """
        Called after protocol has started listening.
        """
        self.transport.setTTL(5)
        self.transport.joinGroup(self.multicast_address)


    def datagramReceived(self, datagram, address):
        self.__packet_handler(datagram, address)
