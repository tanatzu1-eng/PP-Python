from fastapi import FastAPI
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from .routers.articulo_router import router as articulo_router
from .routers.proveedor_router import router as proveedor_router
from .database import engine
from .models.articulo import Articulo, Proveedor # no se usa en el codigo pero hay que importarlo para que main lo tenga


# ========================================================================================================
# cors:
# ========================================================================================================
app = FastAPI()

app.title = "Practico 7 - Tablas Relacionadas"

app.include_router(articulo_router)
app.include_router(proveedor_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = False,
    allow_methods=["*"],
    allow_headers=["*"]
)
# ========================================================================================================


SQLModel.metadata.create_all(bind = engine)
