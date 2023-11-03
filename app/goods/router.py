from fastapi import APIRouter, Depends
from app.root.db import AsyncSession, get_async_session
from app.root.exceptions import InternalServerError
from app.goods.utils import GoodsManager
from .schemes import GoodCreateScheme, CategoryCreateScheme, TagCreateScheme
from typing import List
from logger import logger


goods_router = APIRouter(
    prefix='/api/goods',
    tags=['Goods']
)

@goods_router.post('/new_category')
async def add_category(new_category: CategoryCreateScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        manager = GoodsManager(session)
        await manager.new_category(new_category)

    except Exception as error:
        logger.error(error)
        return InternalServerError()

@goods_router.post('/new_tag')
async def add_tag(new_tag: TagCreateScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        manager = GoodsManager(session)
        await manager.new_tag(new_tag)

    except Exception as error:
        logger.error(error)
        return InternalServerError()


@goods_router.post('/import_tags')
async def import_tags(new_tags: List[TagCreateScheme], session: AsyncSession = Depends(get_async_session)):
    try:
        manager = GoodsManager(session)
        for tag in new_tags:
            await manager.new_tag(tag)
    except Exception as error:
        logger.error(error)
        return InternalServerError()

@goods_router.post('/new_good')
async def add_good(new_good: GoodCreateScheme, session: AsyncSession = Depends(get_async_session)):
    print(new_good)
    try:
        manager = GoodsManager(session)
        await manager.new_good(new_good)

    except Exception as error:
        logger.error(error)
        return InternalServerError()


@goods_router.post('/import_goods')
async def import_goods(new_goods: List[GoodCreateScheme], session: AsyncSession = Depends(get_async_session)):
    try:
        manager = GoodsManager(session)
        for good in new_goods:
            await manager.new_good(good)

    except Exception as error:
        logger.error(error)
        return InternalServerError()


# @goods_router.post('/import_goods')
# async def import_goods(new_goods: List[GoodCreateScheme], session: AsyncSession = Depends(get_async_session)):
#     print(new_goods)
#     try:
#         manager = GoodsManager(session)
#         await manager.import_goods(new_goods)

#     except Exception as error:
#         logger.error(error)
#         return InternalServerError()

