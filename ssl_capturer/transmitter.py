from twisted.internet import reactor
from twisted.protocols import amp

class Push(amp.Command):
    arguments = [('field_id', amp.String()),
                 ('frame', amp.String())]
    #response = [('status', amp.String())]

def gotResult(result):
    print 'total:', result['total']
    #reactor.stop()

def error(reason):
    print "Something went wrong"
    print reason
    reactor.stop()
