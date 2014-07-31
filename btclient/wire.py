import socket
from Torrent import Torrent
from response_handler import ResponseHandler
import requests
import struct


class Handshake(object):
    def __init__(self, torrent):
        self.pstr ='BitTorrent protocol'
        self.pstrlen = chr(len(self.pstr))
        self.reserved = '\x00\x00\x00\x00\x00\x00\x00\x00'
        self.info_hash = torrent.info_hash
        self.peer_id= torrent.peer_id


    def __str__(self):
        fields = [self.pstrlen, self.pstr, self.reserved, self.info_hash, self.peer_id]
        return ''.join(['%s' % field for field in fields])


class Message(object):
    '''
    All of the remaining messages in the protocol take the form of:
    <length prefix>
    <message ID>
    <payload>

    The length prefix is a four byte big-endian
    value. The message ID is a single decimal byte. The payload is message
    dependent.
    '''



    #length_prefix
    #message_id
    #payload

#step 1: send interested message
def send_interested():
    '''
    interested
    interested: <len=0001><id=2>
    The interested message is fixed-length and has no payload.
    '''
    values = (1, 2)
    packer = struct.Struct('>I B')
    packed_data = packer.pack(*values)
    return packed_data


messages = {0: 'choke',
        1: 'unchoke',
        2: 'interested',
        3: 'not interested',
        4: 'have',
        5: 'bitfield',
        6: 'request',
        7: 'piece',
        8: 'cancel',
        9: 'port'}


def message_decode(received):
    packer = struct.Struct('>I B')
    return packer.unpack(received[:5])


# hacky stuff to clean up later.
def get_msg():
    t = Torrent('../torrent/flagfromserver.torrent')
    t.make_request()

    # make request, get response, handle response
    r = requests.get(t.request)
    rh = ResponseHandler(r)
    rh.get_peer_ip()

    # get handshake
    h = Handshake(t)

    #pick ip and port from peers
    ip = rh.ips[-1][0]
    port = rh.ips[-1][1]

    # socket connection and send data
    s = socket.socket()
    s.connect((ip, port))
    s.sendall(str(h))

    # receive data back and pretty print 
    recv = s.recv(100)
    print 'Handshake received: %s' % (recv.__repr__(), )


    s.sendall(send_interested())
    recv = s.recv(10000)
    prefix, message = message_decode(recv)
    return recv

if __name__ == '__main__':
    recv = get_msg()
    #print recv.__repr__()
