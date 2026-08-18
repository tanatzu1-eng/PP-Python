from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field



app = FastAPI()


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


database = [ # tienda de figuras de accion
    {"id": 0, "nombre": "Thorfinn", "precio": 100, "stock": True},
    {"id": 1, "nombre": "Monkey D. Luffy", "precio": 200, "stock": True},
    {"id": 2, "nombre": "Aang", "precio": 300, "stock": True},
    {"id": 3, "nombre": "Heimerdinger", "precio": 400, "stock": True},
    {"id": 4, "nombre": "Nomad", "precio": 500, "stock": False},
    {"id": 5, "nombre": "Ray", "precio": 600, "stock": False},
]


error_responses = {
    404: {
        "description": "producto no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "el id ingresado no coincide con el de ningun producto en la base de datos"
                }
            }
        }
    },
    409: {
        "description": "conflicto de datos",
        "content": {
            "application/json": {
                "example": {
                    "detail": "nombre/id ingresado == database[nombre]/database[id]"
                }
            }
        }
    }
}


PARAMETROS_ID = Annotated[int, Field(ge = 0)]
PARAMETROS_NOMBRE = Annotated[str, Field(min_length = 1, max_length = 30)]
PARAMETROS_PRECIO = Annotated[float, Field(gt = 0)]
PARAMETROS_STOCK = Annotated[bool, Field(default = True)]

class ArticuloSchema(BaseModel):
    nombre: PARAMETROS_NOMBRE
    precio: PARAMETROS_PRECIO
    stock: PARAMETROS_STOCK

class UpdateSchema(BaseModel):
    id: PARAMETROS_ID
    nombre: PARAMETROS_NOMBRE
    precio: PARAMETROS_PRECIO
    stock: PARAMETROS_STOCK



@app.get("/database")
async def obtener_database() -> list[UpdateSchema]:
    return database


@app.get("/database/{id}", response_model = ArticuloSchema, responses = error_responses)
async def obtener_detalles_producto(
    id: Annotated[int, Path(ge = 0,
                            description = "descripcion descriptiva que describe todo lo descriptivamente necesario para describir la descripcion")]) -> ArticuloSchema:

    for producto in database:
        if id == producto["id"]:
            return producto

    raise HTTPException(status_code = 404,
                        detail = "el id no coincide con ningun producto existente")


@app.post("/database", response_model = UpdateSchema, responses = error_responses)
async def aniadir_item(item: UpdateSchema) -> ArticuloSchema:

    for producto in database:
        if producto["nombre"] == item.nombre:
            raise HTTPException(status_code = 409,
                                detail = "el nombre es identico al de otro producto")

        if producto["id"] == item.id:
            raise HTTPException(status_code = 409,
                                detail = "el id ya esta asignado a otro producto")

    database.append({"id": item.id,
                     "nombre": item.nombre,
                     "precio": item.precio,
                     "stock": item.stock})
    return item


@app.put("/database", response_model = UpdateSchema, responses = error_responses)
async def reemplazar_item(item: UpdateSchema) -> ArticuloSchema:

    for producto in database:
        if producto["id"] == item.id:
            producto["nombre"] = item.nombre
            producto["precio"] = item.precio
            producto["stock"] = item.stock
            return item
        
    raise HTTPException(status_code = 404,
                        detail = "el id ingresado no coincide con ningun producto de la base de datos")


@app.delete("/database/{id}", response_model = UpdateSchema, responses = error_responses)
async def borrar_item(id: Annotated[int, Path(ge = 0,
                                              description = "es un id :v")]) -> ArticuloSchema:

    for producto in database:
        if producto["id"] == id:
            database.remove(producto)
            return producto
    
    raise HTTPException(status_code = 404,
                        detail = "el id ingresado no coindide con ningun producto de la base de datos")
