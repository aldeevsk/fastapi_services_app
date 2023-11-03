from fastapi import FastAPI
from app.html.router import html_router
from app.goods.router import goods_router

routers_list = [html_router, goods_router]

def setup_routers(app: FastAPI):
    for router in routers_list:
        app.include_router(router)