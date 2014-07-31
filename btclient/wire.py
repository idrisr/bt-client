from Torrent import Torrent

    def __init__(self):
        am_choking


class Peer(object):
    def __init__(self):
        self.am_choking = 1
        self.am_interested = 0
        self.peer_choking = 1
        self.peer_interested = 0


'''
class Handshake(object):
    def __init__(self):
        self.pstr ='BitTorrent protocol'
        self.pstrlen = chr(len(self.pstr))
        self.reserved='\x00\x00\x00\x00\x00\x00\x00\x00'
        self.info_hash='+\x15\xca+\xfdH\xcd\xd7m9\xecU\xa3\xab\x1b\x8aW\x18\n\t'
        self.peer_id= 'aaaaaaaaaaaaaaaaaaaa'


    def __str__(self):
        fields = [self.pstrlen, self.pstr, self.reserved, self.info_hash, self.peer_id]
        return ''.join(['%s' % field for field in fields])


if __name__ == '__main__':
    h = Handshake()
    print repr(str(h))
