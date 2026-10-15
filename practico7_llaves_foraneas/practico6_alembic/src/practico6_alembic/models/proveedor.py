from sqlmodel import Field, Relationship, SQLModel

from ..schemas.esquemas import PARAMETROS_NOMBRE


class ProveedorBase(SQLModel):
    nombre: str = PARAMETROS_NOMBRE


class Proveedor(ProveedorBase, table = True):
    id: int | None = Field(default = None, primary_key = True)
    articulos: list["Articulo"] | None = Relationship(back_populates = "proveedor")


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorPublic(ProveedorBase):
    id: int


class ProveedorUpdate(SQLModel):
    nombre: str | None = None
