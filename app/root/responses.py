from fastapi import status
from pydantic import BaseModel, Field
from typing import List


# Success responses
class Success(BaseModel):
    status_code: int = status.HTTP_200_OK
    status: str = "Ok"
    detail: str = "Success"


class Data(BaseModel):
    status_code: int = status.HTTP_200_OK
    status: str = "Ok"
    detail: str = "Success"
    payload: List or dict

class Created(BaseModel):
    status_code: int = status.HTTP_201_CREATED
    status: str = "Ok"
    detail: str or None


# Error responses
class NoContentScheme(BaseModel):
    status_code: int = status.HTTP_204_NO_CONTENT
    status: str = "Error"
    detail: str = "Not found!"


class BadRequest(BaseModel):
    status_code: int = status.HTTP_400_BAD_REQUEST
    status: str = "Error"
    detail: str = "Bad request!"


class Forbidden(BaseModel):
    status_code: int = status.HTTP_403_FORBIDDEN
    status: str = "Error"
    detail: str = "Forbidden!"


class NotFound(BaseModel):
    status_code: int = status.HTTP_404_NOT_FOUND
    status: str = "Error"
    detail: str = "Not found!"


class Unauthorized(BaseModel):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    status: str = "Error"
    detail: str = "Unauthorized!"
