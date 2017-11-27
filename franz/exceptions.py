class BaseFranzException(Exception):
    pass


class InvalidMessage(BaseFranzException):
    pass


class SerializationError(BaseFranzException):
    pass
