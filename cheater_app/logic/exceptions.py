from datetime import datetime


class BaseCheaterException(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.timestamp = datetime.now()


class NotSupportedCountryException(BaseCheaterException):
    pass


class InvalidLetterException(BaseCheaterException):
    pass


class IncorrectlyFormattedFileException(BaseCheaterException):
    pass


class WordDoesNotMatchToPatternException(BaseCheaterException):
    pass


class NoMatchingRightAngleException(BaseCheaterException):
    pass


class NotRightAnglePatternException(BaseCheaterException):
    pass


class NotPartOfBridgePatternException(BaseCheaterException):
    pass


class IncorrectMoveException(BaseCheaterException):
    pass


