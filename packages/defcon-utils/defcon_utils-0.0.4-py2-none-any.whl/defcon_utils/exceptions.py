
class BaseException(Exception):
    pass

# EMAIL EXCEPTIONS
class MailException(BaseException):
    pass


class InvalidLoginException(MailException):
    pass


class InvalidMailReceiverException(MailException):
    pass


class NoMailObjectException(MailException):
    pass


class MailNotSentException(MailException):
    pass