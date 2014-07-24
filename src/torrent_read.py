from bencode import bencode, bdecode
from hashlib import sha1
from urllib import quote, urlencode
import requests
import sys


class Torrent(object):

    def __init__(self, file_name):
        self.file_name = file_name


    def get_uploaded(self):
        if not hasattr(self, 'uploaded'):
            self.uploaded = 0

    def get_announce(self):
        pass


    def get_compact(self):
        if not hasattr(self, 'compact'):
            self.compact = 1


    def get_port(self):
        if not hasattr(self, 'port'):
            self.port = 6881


    def get_event(self):
        """ started, completed, or stopped """
        if not hasattr(self, 'event'):
            self.event = 'started'


    def get_downloaded(self):
        if not hasattr(self, 'downloaded'):
            self.downloaded = 0


    def get_peer_id(self):
        if not hasattr(self, 'peer_id'):
            self.peer_id = 's' * 20


    def get_left(self):
        if not hasattr(self, 'left'):
            self.left = 123456789

    def get_info_hash(self):
        self.info_hash = sha1(bencode(t.info)).digest()


    def bdecode(self):
        try:
            file_content = open(self.file_name, 'r').read()
            content = bdecode(file_content)
        except IOError:
            print 'file not found'
            sys.exit(1)

        # TODO: better way to make all dicts into objects, ie avoid torrent.info['name']
        for k, v in content.items():
            setattr(self, k, v)


    def make_request(self, **args):
        '''
            uploaded 0 - when is this not 0?
            compact = 1
            port between 6881 and 6889
            info_hash 
            event: started completed stopped
            downloaded: total amount downloaded so far
            peer_id: A string of length 20 which this downloader uses as its id.
                Each downloader generates its own id at random at the start of a new
                download. Don't forget to URL-encode this.

            left: number of bytes left
        '''
        d = {'uploaded': self.get_uploaded,
                'compact': self.get_compact,
                'port': self.get_port,
                'event': self.get_event,
                'downloaded': self.get_downloaded, 
                'peer_id': self.get_peer_id,
                'left':  self.get_left,
                'info_hash': self.get_info_hash
                }

        #make sure all the values we need are set 
        for v in d.values():
            v()

        request_params = {}

        for k in d:
            request_params.update({k: getattr(self, k)})

        self.request = '%s?%s' % (self.announce, urlencode(request_params), )


if __name__ == '__main__':
    filename = '../torrent/flagfromserver.torrent'
    t = Torrent(filename)
    t.bdecode()
    t.make_request()
    print t.request
    r = requests.get(t.request)
    print r.text
