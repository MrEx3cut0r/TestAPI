class DomainException(Exception):
    pass

class PriceNotFoundException(DomainException):
    pass


class InvalidTickerException(DomainException):
    pass


class InvalidPriceException(DomainException):
    pass