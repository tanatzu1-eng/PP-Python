from sqlmodel import Field, SQLModel


# ========================================================================================================
# articulo:
# ========================================================================================================
class ArticuloBase(SQLModel):
    nombre: str
    precio: float
    disponible: bool = True
    marca: str | None = None # le habilito None porque los registros ya creados van a aparecer con un None en este campo

class Articulo(ArticuloBase, table = True):
    id: int | None = Field(default = None, primary_key = True)

class ArticuloCreate(ArticuloBase):
    pass

class ArticuloPublic(ArticuloBase):
    id: int

class ArticuloUpdate(SQLModel): # el profe no pide esto, pero lo considero muy util para actualizar muchos datos, como cuando se hace una migracion
    nombre: str | None = None
    precio: float | None = None
    disponible: bool | None = None
    marca: str | None = None
# ========================================================================================================
