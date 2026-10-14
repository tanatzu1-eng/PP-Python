from fastapi import FastAPI
from sqlmodel import SQLModel, Session
from fastapi.middleware.cors import CORSMiddleware

from .routers.articulo_router import router
from .database import engine
from .models.modelos import Articulo


# ========================================================================================================
# cors:
# ========================================================================================================
app = FastAPI()

app.title = "Practico 6 - Alembic"

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = False,
    allow_methods=["*"],
    allow_headers=["*"]
)
# ========================================================================================================


SQLModel.metadata.create_all(bind = engine)
