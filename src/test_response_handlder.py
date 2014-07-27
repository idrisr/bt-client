from response_handler import ResponseHandler
from unittest import TestCase
from nose.tools import with_setup
from bencode import bdecode


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
        r = ResponseHandler()
        r._content = 'd8:completei1e10:downloadedi1e10:incompletei1e8:intervali1743e12:min intervali871e5:peers12:J\xd4\xb7\xba\x1a\xe1`~h\xdb\xea9e'
        r.get_peer_ip()
        exp = [(74, 212, 183, 186, 26, 225), (96, 126, 104, 219, 234, 57)]
        ans = r.ip
        self.assertListEqual(exp, ans)
