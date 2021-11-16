class InfiniteLoopException(Exception):
    pass

class EndStateNotException(Exception):
    pass

class OutOfTapeHeadException(Exception):
    """Head out of tape."""
    pass

class NotImplementedHeadMoveException(Exception):
    pass
