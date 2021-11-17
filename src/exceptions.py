class InfiniteLoopException(Exception):
    pass

class OutOfTapeHeadException(Exception):
    """Head out of tape."""
    pass

class NotImplementedHeadMoveException(Exception):
    pass

class BadChar(Exception):
    """Not Valid character"""


class EndStateNotException(Exception):
    pass