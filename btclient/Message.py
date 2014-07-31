from abc import ABCMeta, abstractmethod

class BaseMessage(object):
    """ Abstract Base Class for specified message classes"""
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')

    @abstractmethod
    def is_message_for(cls, id):
        raise NotImplementedError


    def __repr__(self):
        return "%s" % (self.__class__.__name__, )


class MessageKeepAlive(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageKeepAlive, self).__init__(**kwargs)
        # TODO: determine right place to set len
        #self.len_ = kwargs.get('len_')

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
    def __init__(self, **kwargs):
        super(MessageHave, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 4:
            return True
        return False

class MessageBitField(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageBitField, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 5:
            return True
        return False

class MessageRequest(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageRequest, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 6:
            return True
        return False

class MessagePiece(BaseMessage):
    def __init__(self, **kwargs):
        super(MessagePiece, self).__init__(**kwargs)

    @classmethod
    def is_message_for(cls, id):
        if id == 7:
            return True
        return False

class MessageCancel(BaseMessage):
    def __init__(self, **kwargs):
        super(MessageCancel, self).__init__(**kwargs)

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

def MessageFactory(id):
    """
    Factory function to iterate through Messages's subclasses at run-time
    and return an instance of the matching subclass.
    """

    for cls in BaseMessage.__subclasses__():
        if cls.is_message_for(id):
            return cls(id=id)

    raise ValueError, "Could not find a message type for message id: %s" % id


if __name__ == '__main__':
    ids = [None]
    ids.extend(range(10))
    for id in ids:
        print MessageFactory(id).__class__.__name__
