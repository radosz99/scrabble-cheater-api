from functools import wraps
from time import time


class NotSupportedCountry(Exception):
    pass


class IncorrectlyFormattedFile(Exception):
    pass


class WordDoesNotMatchToPattern(Exception):
    pass


class NoMatchingRightAngle(Exception):
    pass


class NotRightAnglePattern(Exception):
    pass


class NotPartOfBridgePattern(Exception):
    pass


class IncorrectMove(Exception):
    pass


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        # print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        print('func:%r took: %2.4f sec' % (f.__name__, te - ts))
        return result

    return wrap