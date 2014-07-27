from torrent_read import Torrent
from bencode import bdecode
import sys
import requests


class ResponseHandler(object):
    def __init__(self, response):
        #TODO: figure out right way to handle this
        if response.status_code != 200:
            print 'invalid request'
            sys.exit(1)
        else:
            for k, v in response.__dict__.items():
                setattr(self, k, v)


    def set_peers(self):
        pass



if __name__ == '__main__':
    try: 
        filename = sys.argv[1]
    except IndexError:
        filename = '../torrent/flagfromserver.torrent'
        #filename = '../torrent/linuxmint-16-cinnamon-dvd-64bit.torrent'

    t = Torrent(filename)
    t.bdecode()
    t.make_request()
    r = requests.get(t.request)
    response = ResponseHandler(r)
