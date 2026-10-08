from sqlmodel import SQLModel, Field


class ArticuloBase(SQLModel): # este es el modelo base que heredan las demas clases
    id: int = Field(default=None)
    nombre: str
    descripcion: str
    precio: float

# =========================================================================================================================================
class Articulo(ArticuloBase, table=True): # para crear el id de un nuevo articulo
    id: int | None = Field(default=None, primary_key=True)

class ArticuloCreate(ArticuloBase): # para crear el resto de un nuevo articulo
    pass
# por que Articulo y ArticuloCreate no estan en la misma clase? porque resuelve problemas de seguridad, principalmente por si hay
# un usuario malintencionado, este podria crear un json con un id inventado y fastapi lo usaria sin cuestionar, pero si separo las
# clases, el usuario no tiene acceso a la clase que crea el id. 
# =========================================================================================================================================

class ArticuloPublic(ArticuloBase): # para mostrar datos al usuario
    id: int