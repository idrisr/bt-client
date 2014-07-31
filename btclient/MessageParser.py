from struct import unpack, Struct
from Message import MessageFactory
from collections import deque
from bitarray import bitarray
from wire import get_msg

"""
>>> input_str = '0xff'
>>> c = BitArray(hex=input_str)
>>> c.bin
'0b11111111'
"""

test_msg =  '\x00\x00\x00\x0b\x05\xbf\xff\xef\xff\xfb\xdf\xbb\xff\xfe\xfe\x00\x00\x00\x05\x04\x00\x00\x00\x01\x00\x00\x00\x05\x04\x00\x00\x00\x13\x00\x00\x00\x05\x04\x00\x00\x00%\x00\x00\x00\x05\x04\x00\x00\x00*\x00\x00\x00\x05\x04\x00\x00\x001\x00\x00\x00\x05\x04\x00\x00\x005\x00\x00\x00\x05\x04\x00\x00\x00'

q = deque(test_msg)
q = deque(get_msg())
"""
Messages
All of the remaining messages in the protocol take the form of 
<length> The length prefix is a four byte big-endian value
<message id> is a single decimal type
<payload> is message dependent
"""

"""
get first 5 bytes
convert into ID and correct Message Class
pass the rest of the message as the Message class desires
"""

# big endian 4 byte int, 1 byte int
len_unpacker = Struct('>I')
id_unpacker = Struct('b')
#payload_unpacker = lambda x: 

b = bitarray()

def msg_left_pop(q, length):
    return ''.join([q.popleft() for x in range(length)])

def pop_len(q):
    return msg_left_pop(q, 4)

def pop_id(q):
    return msg_left_pop(q, 1)

def pop_payload(q, size):
    payload = msg_left_pop(q, size)
    return payload

def get_id_and_msg(msg):
    id = id_unpacker.unpack(msg[0])[-1]
    msg = msg[1:]
    return id, msg

while len(q) > 0:
    msg_len = len_unpacker.unpack(pop_len(q))[-1]

    # is not a keep-alive message
    if msg_len > 0:
        msg = msg_left_pop(q, msg_len)
        id, raw_payload = get_id_and_msg(msg)
    else:
        id = None
        raw_payload = None

    message = MessageFactory(id = id, raw_payload = raw_payload)
    print message
