from pydantic import BaseModel, Field, EmailStr, FileUrl, HttpUrl
from datetime import datetime
from typing import List


class RoleScheme(BaseModel):
    id: int
    label: str
    permissions: List[str]

class UserScheme(BaseModel):
    id: int
    username: str
    full_name: str
    image: FileUrl = Field(default=None)
    email: EmailStr
    hashed_password: str
    role_id: int
    register_date: datetime
    last_visit: datetime
    disabled: bool

class UserFullScheme(BaseModel):
    id: int
    username: str
    full_name: str
    image: FileUrl = Field(default=None)
    email: EmailStr
    hashed_password: str
    role_id: int
    role: RoleScheme
    register_date: datetime
    last_visit: datetime
    disabled: bool
    permissions: List[str]


class UserRegisterScheme(BaseModel):
    username: str
    full_name: str
    image: FileUrl = Field(default=None)
    email: EmailStr
    password: str

class UserLoginScheme(BaseModel):
    email: EmailStr
    password: str

class UserResponseScheme(BaseModel):
    id: int
    username: str
    full_name: str
    image: HttpUrl = Field(default=None)
    email: EmailStr
    register_date: datetime
    last_visit: datetime
    disabled: bool
    role: RoleScheme
    permissions: List[str]
