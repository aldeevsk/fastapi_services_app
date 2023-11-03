from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from app.root.db import AsyncSession, get_async_session
from app.goods.utils import GoodsManager
from fastapi.responses import HTMLResponse


html_router = APIRouter(
    prefix='',
    tags=['HTML']
)

templates = Jinja2Templates(directory="templates")

@html_router.get('/')
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Ынтымак пласт | Ремонтные услуги в Бишкеке", "page": "home", "description": "Услуги по ремонту, по ремонту окон и дверей, сантехническим, и электромонтажным работам"})



@html_router.get('/category/{category_slug}')
async def category_page(request: Request, category_slug: str, session: AsyncSession = Depends(get_async_session)):
    try:
        manager = GoodsManager(session)
        await manager.get_by_category_slug(category_slug)

        category = manager.category
        goods = manager.goods
        tags = manager.tags

        return templates.TemplateResponse("category.html", {"request": request, "title": f"Ынтымак пласт | {category.description}", "category": category, "goods": goods, "tags": tags, "page": category.slug, "description": category.description})
    except HTTPException as error:
        if error.status_code == 404:
            return templates.TemplateResponse("404.html", {"request": request})
