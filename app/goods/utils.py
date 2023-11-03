from fastapi import HTTPException
from sqlalchemy import insert, delete, update, select
from .models import Good, Category, Tag, Work
from .schemes import GoodScheme, GoodCreateScheme, GoodResponseScheme, CategoryCreateScheme, TagCreateScheme
from app.root.db import AsyncSession
from logger import logger
from app.root.exceptions import NotFoundError, DbError, BadRequestError, InternalServerError
from typing import List
import json


class GoodsManager():
    def __init__(self, session: AsyncSession):
        self.category = None
        self.tags = None
        self.goods = None
        self.session = session


    async def get_by_category_slug(self, category_slug: str, offset: int = 0, limit:int = 80):
        try:
            query = select(Category).where(Category.slug == category_slug)
            result = await self.session.execute(query)
            self.category = result.scalar_one_or_none()
            if not self.category:
                raise HTTPException(status_code=404)
            query = select(Tag)
            result = await self.session.execute(query)
            self.tags = result.scalars().all()

            query = select(Good).where(Good.category_id == self.category.id).offset(offset).limit(limit)
            result = await self.session.execute(query)
            goods = result.scalars().all()
            modified_goods = []
            category_tags = []
            for good in goods:
                for tag in self.tags:
                    if good.tag_id == tag.id:
                        good.tag = tag
                        category_tags.append(tag)

                modified_goods.append(good)

            category_tags = set(category_tags)
        
            self.goods = modified_goods
            self.tags = category_tags

            for tag in self.tags:
                print(tag.id)

        except Exception as error:
            logger.error(error)
            raise DbError(detail=error)

    async def new_category(self, category: CategoryCreateScheme):
        if not category:
            raise BadRequestError(detail='Invalid data')

        try:
            new_cat = Category(**category.model_dump())
            self.session.add(new_cat)
            await self.session.commit()
        except Exception as error:
            logger.error(error)
            raise DbError(detail=error)

    async def new_tag(self, tag: TagCreateScheme):
        try:
            new_t = Tag(**tag.model_dump())
            self.session.add(new_t)
            await self.session.commit()
        except Exception as error:
            logger.error(error)
            raise DbError(detail=error)

    async def new_good(self, good: GoodCreateScheme):
        try:
            new_g = Good(**good.model_dump())
            self.session.add(new_g)
            await self.session.commit()
        except Exception as error:
            logger.error(error)
            raise DbError(detail=error)

    async def import_goods(self, goods_list: List[GoodCreateScheme]):
        if not goods_list:
            raise BadRequestError(detail='Goods data no provided')
        try:
            # query = select(Category)
            # result = await self.session.execute(query)
            # db_categories = result.scalars() or []
            # query = select(Tag)
            # result = await self.session.execute(query)
            # db_tags = result.scalars() or []

            new_goods: List[Good] = []
            for item in goods_list:
                good = Good(**item.model_dump())
                new_goods.append(good)

            self.session.add_all(new_goods)
            await self.session.commit()

        except Exception as error:
            logger.error(error)
            raise InternalServerError(detail=error)
