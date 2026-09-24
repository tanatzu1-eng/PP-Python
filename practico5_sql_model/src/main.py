from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from routers.articulos_router import router
from database import Base, engine
from models import models_articulos


Base.metadata.create_all(bind = engine)


app = FastAPI()

app.title = "App"

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)