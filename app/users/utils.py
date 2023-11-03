import jwt
from config import SECRET_KEY, JWT_ALGORITHM
from logger import logger
from fastapi import Request, Response
from .models import User, Role
from app.root.schemes import SuccessScheme
from .schemes import UserResponseScheme, UserScheme, UserLoginScheme, UserFullScheme, UserRegisterScheme
from .exceptions import UserLoginError, UserRegisterError, InternalServerError, UserAuthenticationError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Optional
from functools import wraps

crypt_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],  # Используемые схемы хэширования
    deprecated=["auto"],  # Устаревшие схемы, автоматически заменяемые на более безопасные
    pbkdf2_sha256__default_rounds=10000,  # Количество раундов для PBKDF2-SHA256
    bcrypt__default_rounds=12,  # Количество раундов для bcrypt
    # Указываем секретный ключ
    all__vary_rounds=True,  # Для всех схем, варьировать количество раундов
    all__secret=SECRET_KEY  # Указываем секретный ключ
)

def_expire = datetime.utcnow() + timedelta(minutes=30)

async def create_hashed_password(password: str):
    hashed_password = crypt_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    return crypt_context.verify(password, hashed_password)

def generate_access_token(email: str, permissions: List[str], expire_minutes: int | None = None):
    if expire:
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    else:
        expire = def_expire

    token = jwt.encode({"email": email, "permissons": permissions, "exp": expire,}, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


async def parse_token(token: str):
    if not token:
        raise UserAuthenticationError('Token no provided')
    try:
        payload = await jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        email = payload.get("email")
        permissions = payload.get("permissions")
        return {"email": email, "permissions": permissions}
    except jwt.exceptions.ExpiredSignatureError:
        # Обработка истекшего токена
        raise UserAuthenticationError(detail="Expired token")
    except jwt.exceptions.InvalidTokenError:
        # Обработка недействительного токена
        raise UserAuthenticationError(detail="Invalid token")


def protected(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs["token"]
            if not token:
                raise UserAuthenticationError("Invalid token")
            permissions = await parse_token(token)["permissions"]
            if permission in permissions:
                return await func(*args, **kwargs)
            else:
                raise UserAuthenticationError(detail="Access denied")
        return wrapper
    return decorator


class UserManager:
    def __init__(self, user: UserLoginScheme | UserRegisterScheme | UserScheme, session: AsyncSession):
        if not session:
            raise UserLoginError(detail="session no provided")
        self.session = session

        if not user:
            raise UserLoginError(detail="User data no provided!")
        self.user = user

    async def set_user_data(self):
        if not isinstance(self.user, UserLoginScheme):
            return UserRegisterError(detail="Invalid user data")

        query = select(User).where(User.email == self.user.email).options(selectinload(User.role))
        result = await self.session.execute(query)
        current_user = result.scalar_one_or_none()

        if not current_user:
            raise UserLoginError(detail="User not found")

        self.user_data: UserScheme = {
            **current_user,
            "role": current_user.role,
            "permissions": current_user.role.permissions
        }

        response_data = current_user.__dict__.pop("hashed_password")
        self.user_response_data: UserResponseScheme = {
            **response_data,
            "role": current_user.role,
            "permissions": current_user.role.permissions
        }
        return self.user_data


    async def register(self):
        if not isinstance(self.user, UserRegisterScheme):
            return UserRegisterError(detail="Invalid user data")

        try:
            new_user = User(**self.user)
            self.session.add(new_user)
            await self.session.commit()
            user_data = await self.set_user_data()
            return user_data

        except Exception as error:
            logger.error(error)
            raise UserRegisterError(detail="Error in User register")


    async def login(self, response: Response):
        if not isinstance(self.user, UserLoginScheme):
            raise UserRegisterError(detail="Invalid user data")

        if not self.user_data:
            self.user_data = await self.set_user_data()

        if self.user:
            if not verify_password(self.user.password, self.user_data.hashed_password):
                raise UserLoginError(detail="Invalid login or password!")

            token = generate_access_token(self.user_data.email, self.user_data.permissions)
            if not token:
                raise InternalServerError(detail="Error in generate token")
            response.headers["Authorization"] = f"Bearer {token}"
            return self.user_response_data


    async def authenticate(self, request: Request):
        if not self.user_data:
            self.user_data = await self.set_user_data()

        try:
            token = request.headers.get("Authorization").split("Bearer ")[1]
            if not token:
                raise UserLoginError(detail="User no authentcated, login please")

            token_data = parse_token(token)
            return token_data

        except Exception as error:
            logger.error(error)
            raise UserLoginError(detail=f"Authentication error - {error}")


    async def update(self):
        if not isinstance(self.user, UserScheme):
            raise UserRegisterError(detail="Invalid user data")

        if not self.user_data:
            self.user_data = await self.set_user_data()

        try:
            smt = update(User).where(User.email == self.user_data.email).values(**self.user)
            await self.session.execute(smt)
            return True
        except Exception as error:
            raise InternalServerError(detail=error)


    async def delete(self):
        if not isinstance(self.user, UserScheme):
            raise UserRegisterError(detail="Invalid user data")

        if not self.user_data:
            self.user_data = await self.set_user_data()

        try:
            smt = delete(User).where(User.email == self.user_data.email)
            await self.session.execute(smt)
            return True
        except Exception as error:
            raise InternalServerError(detail=error)
