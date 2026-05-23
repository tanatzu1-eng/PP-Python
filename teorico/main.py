from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "Mi primera API"  # Así cambia el nombre en /docs



# ================================================================================================================
# agregamos el intermediario entre fastapi y la web para evitar error de Cors
# ================================================================================================================
app.add_middleware(
    CORSMiddleware,
    # esto agrega el intermediario CORSMiddleware

    allow_origins=[
        "http://127.0.0.1:5500",  # entorno desarrollo (mi pc)
        "https://faculemo.github.io/front",  # entorno producción del profe
        # tambien se puede poner un asterisco "*" y eso permitiria cualquier origen (no se recomienda jamas)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # con estos allows estoy autorizando a que use ese origin, las credenciales y cualquier tipo de metodo y header

)
# ================================================================================================================



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
# definimos not_found para reutilizar:
# ================================================================================================================
not_found = {
    404: {
    # al poner el status_code, fastapi sabe de que es el error y lo usa situacionalmente

        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Artículo no encontrado",
                }
            }
        },
    },
}

# normalmente, tendria que crear un disenio personalizado para cada error, no solo para el 404, pero es solo un ejemplo
# ================================================================================================================



# ================================================================================================================
# creamos una clase reutilizando los parametros preestablecidos:
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


@app.get("/articulos/{id}", response_model = ArticuloSchema, responses = not_found)

# responses y response_model son funciones de fastapi

# response_model indica la respuesta predeterminada que debe devolver la funcion

# responses son las posibles respuestas que puede dar la funcion dependiendo del error, en este caso solo hice not_found, pero podria ser:
# responses={
#    **not_found,
#    **bad_request,
#    **server_error
# }


async def get_articulos_by_id(
    id: Annotated[int, Path(gt=0)]):

    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

# la flechita (->) es una funcion de python que indica  el tipo de dato que debe retornar una funcion, en este caso el response_model debe tener la estructura del ArticuloSchema
# ================================================================================================================
