from fastapi import APIRouter, Depends, Response, Request
from .schemes import UserRegisterScheme, UserLoginScheme, UserResponseScheme, UserScheme
from app.root.db import AsyncSession, get_async_session
from app.root.responses import Success, Data
from app.root.exceptions import UserRegisterError, InternalServerError
from .utils import UserManager, protected
from logger import logger


user_router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)

@user_router.get('/')
async def get_users():
    return {'users': ['users']}


@user_router.post('/register')
async def user_register(user: UserRegisterScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        manager = UserManager(user, session)
        user_data = await manager.register()
        if not user_data:
            return UserRegisterError(detail="User not register")

        return Success(detail="User registered successfull")

    except Exception as error:
        logger.error(error)
        return error


@user_router.post('/login')
async def user_login(response: Response, user: UserLoginScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        manager = UserManager(user, session)
        user_response_data = await manager.login(response)
        return Data(detail="User registered successfull", payload=user_response_data)

    except Exception as error:
        logger.error(error)
        return InternalServerError()


@user_router.post('/update')
@protected("update")
async def update_user(user: UserScheme):
    try:
        manager = UserManager()
        await manager.update(user)
        return Success(detail="User data updated successfull")
    except Exception as error:
        logger.error(error)
        return InternalServerError()
