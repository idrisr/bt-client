from btclient.response_handler import ResponseHandler
from btclient.torrent_read import Torrent
from unittest import TestCase
from nose.tools import with_setup
from bencode import bdecode
import os
import requests


class TestResponseHandler(TestCase):

    #TODO: how to use setup and teardowns?
    @classmethod
    def setup(cls):
        print 'in setup'
        r = ResponseHandler()
        r._content = 'd8:completei1e10:downloadedi1e10:incompletei1e8:intervali1743e12:min intervali871e5:peers12:J\xd4\xb7\xba\x1a\xe1`~h\xdb\xea9e'
        self.response = r


    @classmethod
    def teardown(cls):
        pass


    def test_set_peers(self):
        filename = os.path.join(os.environ['HOME'], 'bt-client/torrent/flagfromserver.torrent')
        t = Torrent(filename)
        t.make_request()
        response = requests.get(t.request)
        response_handler = ResponseHandler(response)
        response_handler.parse_response(response)
        t.make_request()
        r = ResponseHandler(response)
        r._content = 'd8:completei1e10:downloadedi1e10:incompletei1e8:intervali1743e12:min intervali871e5:peers12:J\xd4\xb7\xba\x1a\xe1`~h\xdb\xea9e'
        r.get_peer_ip()
        exp = ('96.126.104.219', 234 * 256 + 57, )
        ans = r.ips[-1]
        self.assertTupleEqual(exp, ans)
