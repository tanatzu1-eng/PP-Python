from sqlmodel import Field, Relationship, SQLModel

from .proveedor import Proveedor


class ArticuloBase(SQLModel):
    nombre: str
    precio: float
    disponible: bool = True
    marca: str | None = None
    proveedor_id: int | None = Field(default = None, foreign_key = "proveedor.id")


class Articulo(ArticuloBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    proveedor: Proveedor | None = Relationship(back_populates = "articulos")


class ArticuloCreate(ArticuloBase):
    pass


class ArticuloPublic(ArticuloBase):
    id: int


class ArticuloUpdate(SQLModel): # el profe no pide ni menciona esta clase, pero lo considero muy util para actualizar muchos datos, como cuando se hace una migracion
    nombre: str | None = None
    precio: float | None = None
    disponible: bool | None = None
    marca: str | None = None
    proveedor_id: int | None = None
