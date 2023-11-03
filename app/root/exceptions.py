from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError


class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Something went wrong! Please try again letter"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestError(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ForbiddenError(HTTPException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class DbError(SQLAlchemyError):
    def __init__(self, detail: str = "Something went wrong! Please try again letter"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class DbNotFoundError(NotFoundError):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)



class UserAuthenticationError(ForbiddenError):
    def __init__(self, detail: str):
        super().__init__(detail=detail)

class UserNotFoundError(ForbiddenError):
    def __init__(self):
        super().__init__(detail='User not found')

class UserLoginError(ForbiddenError):
    def __init__(self, detail: str):
        super().__init__(detail=detail)


class UserRegisterError(BadRequestError):
    def __init__(self, detail: str):
        super().__init__(detail=detail)

class PermissionError(ForbiddenError):
    def __init__(self):
        super().__init__(detail='Access denied')
