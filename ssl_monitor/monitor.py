import json

from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.protocol import Factory


from processing import sanitize_packet, get_latest_state
from websockets import sockets

class Push(amp.Command):
    arguments = [('field_id', amp.String()),
                 ('frame', amp.String())]
    #response = [('status', amp.String())]

class AMP_SSLMonitorProtocol(amp.AMP):
    def connectionLost(self, reason):
        print "Connection lost"

    @Push.responder
    def PUSH(self, field_id, frame):
        d = sanitize_packet(frame)
        print sockets

        if field_id in sockets:
            for i in sockets[field_id]:
                i.write_message(json.dumps(d))
        return {'status':'ok'}


class AMP_SSLMonitorFactory(Factory):
    def buildProtocol(self, addr):
        print "New protocol Instance"
        return AMP_SSLMonitorProtocol()
