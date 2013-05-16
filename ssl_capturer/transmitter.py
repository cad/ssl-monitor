from twisted.internet.protocol import Protocol, ClientFactory
from sys import stdout

class Transmitter(Protocol):
    def dataReceived(self, data):
        pass
        

class TransmitterFactory(ClientFactory):
    
    def __init__(self):
        self.protocols = []
    
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        protocol = Transmitter()
        self.protocols.append(protocol)
        return protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        
    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        
