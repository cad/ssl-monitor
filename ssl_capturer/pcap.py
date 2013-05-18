import dpkt
from twisted.internet import reactor, defer

DEFAULT_FPATH = '/home/cad/dump.pcap'


class Replayer(object):
    """Replays the vision packets from a pre-recorded pcap file."""
    
    def __init__(self, pcap_f):
        self.f = open(pcap_f) if type(pcap_f) == str else pcap_f
        self.packet_index = []

        self.__packet_reader = None
        
        self.__read_packets()
        self.__create_index()

    def __read_packets(self):
        self.__packet_reader = dpkt.pcap.Reader(self.f)


    def __create_index(self):
        # we can add extra conditions down here such as if udp[x][1].dport == 10020 etc.
        packets = filter(lambda index: type(index[1]) == dpkt.ethernet.Ethernet, self.__packet_reader)
        packets = filter(lambda index: type(index[1]) == dpkt.ip.IP, packets)
        packets = filter(lambda index: type(index[1]) == dpkt.udp.UDP, packets)

        for ts, packet in self.__packet_reader:
            frame = dpkt.ethernet.Ethernet(packet)
            if type(frame.data.data) == dpkt.udp.UDP:
                self.packet_index.append((ts, frame.ip.udp.data))
        

    def replay_packets(self, callback):
        margin = self.packet_index[0][0]
        for packet in self.packet_index:
            tdelta = packet[0] - margin
            reactor.callLater(tdelta, callback, packet[1], '127.0.0.1')
            
        
        


if __name__ == '__main__':
    def a(x, address):
        print x
        
    replayer = Replayer(DEFAULT_FPATH)
    replayer.replay_packets(a)
    reactor.run()
