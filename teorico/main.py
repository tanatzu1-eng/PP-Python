from typing import Annotated
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Mi primera API"  # Así cambia el nombre en /docs


# ================================================================================================================
# abreviamos los Annotated para no tener que escribir tanto:
# ================================================================================================================
STR_CORTITO = Annotated[str, Field(max_length=30)]
PRECIO_PVP = Annotated[float, Field(lt=999999)]
BOOL_ACTIVO = Annotated[bool, Field(description="Disponible?")]

# Annotates sirve para agrupar la informacion de un dato, se puede meter el tipo de dato y el Field
# Field contiene los parametros del dato (condiciones para que sea valido) como gt y/o deprecated
# ================================================================================================================


# ================================================================================================================
# creamos una clase para reutilizar los parametros preestablecidos:
# ================================================================================================================
class ArticuloSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del articulo", deprecated=True)] 
    nombre: STR_CORTITO
    precio: PRECIO_PVP = 1500
    activo: BOOL_ACTIVO = True

# BaseModel sirve para validar automaticamente los datos que le estoy pasando, sin basemodel directamente no funciona


class ArticuloUpdateSchema(BaseModel):
    nombre: STR_CORTITO
    precio: PRECIO_PVP = 2000
    activo: BOOL_ACTIVO = True
# ================================================================================================================


# ================================================================================================================
# Simulación db supermercado:
# ================================================================================================================
articulos = [
    {"id": 1, "nombre": "Paquete de Arroz", "precio": 2000, "activo": True},
    {"id": 2, "nombre": "Fideos", "precio": 3000, "activo": True},
    {"id": 3, "nombre": "Atún Desmenuzado", "precio": 150.50, "activo": True},
]
# ================================================================================================================


# ================================================================================================================
# funciones:
# ================================================================================================================
@app.get("/articulos")
async def get_articulos() -> list[ArticuloSchema]:
    return articulos


@app.get("/articulos/{id}")
async def get_articulos_by_id(
    id: Annotated[int, Path(gt=0)]) -> ArticuloSchema:
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

# la flechita (->) indica retorno, osea que despues de ese id, la funcion debe retornar los datos de ArticuloScheme
# ================================================================================================================