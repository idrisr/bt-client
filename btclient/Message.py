from abc import ABCMeta, abstractmethod
from struct import Struct, unpack
from bitarray import bitarray
from binascii import b2a_hex

class BaseMessage(object):
    """ Abstract Base Class for specified message classes"""
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.raw_payload = kwargs.get('raw_payload')

    @abstractmethod
    def is_message_for(cls, id):
        raise NotImplementedError


    def __repr__(self):
        return "%s" % (self.__class__.__name__, )

    @staticmethod
    def hex_print(s):
        return b2a_hex(s)


class MessageKeepAlive(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageKeepAlive, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id is None:
            return True
        return False

class MessageChoke(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageChoke, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 0:
            return True
        return False

class MessageUnchoke(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageUnchoke, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 1:
            return True
        return False


class MessageInterested(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageInterested, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 2:
            return True
        return False

class MessageNotInterested(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageNotInterested, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 3:
            return True
        return False

class MessageHave(BaseMessage):
    payload_unpacker = Struct('>I')

    def __init__(self, **kwargs):
        super(MessageHave, self).__init__(**kwargs)
        self.payload = self.payload_unpacker.unpack(self.raw_payload)[-1]


    @classmethod
    def is_message_for(cls, id):
        if id == 4:
            return True
        return False

    def __repr__(self):
        return "%s: %r" % (self.__class__.__name__, BaseMessage.hex_print(self.raw_payload),)

class MessageBitField(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageBitField, self).__init__(**kwargs)
        self.payload = bitarray()
        self.payload.frombytes(self.raw_payload)


    @classmethod
    def is_message_for(cls, id):
        if id == 5:
            return True
        return False

    def __repr__(self):
        return "%s: %r" % (self.__class__.__name__, BaseMessage.hex_print(self.raw_payload),)

class MessageRequest(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageRequest, self).__init__(**kwargs)

    def set_properties(self, **kwargs):
        self.index = kwargs.get('index')
        self.begin = kwargs.get('begin')
        self.length = kwargs.get('length')

    @classmethod
    def is_message_for(cls, id):
        if id == 6:
            return True
        return False

class MessagePiece(BaseMessage):
    def __init__(self, **kwargs):
        super(MessagePiece, self).__init__(**kwargs)

    def set_properties(self, **kwargs):
        self.index = kwargs.get('index')
        self.begin = kwargs.get('begin')
        self.block = kwargs.get('block')

    @classmethod
    def is_message_for(cls, id):
        if id == 7:
            return True
        return False

class MessageCancel(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageCancel, self).__init__(**kwargs)

    def set_properties(self, **kwargs):
        self.index = kwargs.get('index')
        self.begin = kwargs.get('begin')
        self.block = kwargs.get('block')

    @classmethod
    def is_message_for(cls, id):
        if id == 8:
            return True
        return False

class MessagePort(BaseMessage):
    def __init__(self, **kwargs):
        super(MessagePort, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 9:
            return True
        return False

def MessageFactory(**kwargs):
    """
    Factory function to iterate through Messages's subclasses at run-time
    and return an instance of the matching subclass.
    """
    for cls in BaseMessage.__subclasses__():
        if cls.is_message_for(kwargs.get('id')):
            return cls(**kwargs)

    raise ValueError, "Could not find a message type for message id: %s" % id
