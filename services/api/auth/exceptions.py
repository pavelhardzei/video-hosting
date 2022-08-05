from base.exceptions import HTTPExceptionWithCode


class InvalidCredentialsException(HTTPExceptionWithCode):
    pass


class UserNotFoundException(HTTPExceptionWithCode):
    pass


class AlreadyExistsException(HTTPExceptionWithCode):
    pass


class InvalidTokenException(HTTPExceptionWithCode):
    pass


class UserInactiveException(HTTPExceptionWithCode):
    pass


class AlreadyVerifiedException(HTTPExceptionWithCode):
    pass


class TimeoutErrorException(HTTPExceptionWithCode):
    pass
