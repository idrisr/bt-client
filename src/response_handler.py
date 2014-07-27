from torrent_read import Torrent
from bencode import bdecode
import sys
import requests


class ResponseHandler(object):
    def parse_response(self, response):
        #TODO: figure out right way to handle this
        if response.status_code != 200:
            print 'invalid request'
            sys.exit(1)
        else:
            for k, v in response.__dict__.items():
                setattr(self, k, v)


    def get_peer_ip(self):
        self.peers = bdecode(self._content)['peers']

        # expect 6 bytes per peer
        assert len(list(self.peers)) % 6 == 0

        #bs = bytearray(self.peers)
        bs = [ord(b) for b in list(self.peers)]

        n = 6
        self.ip = []
        for i in xrange(0, len(bs), n):
            self.ip.append(tuple(bs[i:i+n]))


if __name__ == '__main__':
    try: 
        filename = sys.argv[1]
    except IndexError:
        filename = '../torrent/flagfromserver.torrent'
        #filename = '../torrent/linuxmint-16-cinnamon-dvd-64bit.torrent'

    t = Torrent(filename)
    t.bdecode()
    t.make_request()
    response = requests.get(t.request)
    response_handler = ResponseHandler()
    response_handler.parse_response(response)
    response_handler.get_peer_id()
