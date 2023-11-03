from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.root.router import setup_routers


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="assets")

setup_routers(app)
