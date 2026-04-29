from fastapi import FastAPI, Path, Query, Body

app = FastAPI()

database = [
    {"id": 1, "nombre": "producto1", "precio": 100},
    {"id": 2, "nombre": "producto2", "precio": 200},
    {"id": 3, "nombre": "producto3", "precio": 300},
    {"id": 4, "nombre": "producto4", "precio": 400},
    {"id": 5, "nombre": "producto5", "precio": 500},
]


@app.get('/database/id/{id}')
async def obtener_nombre(id: int = Path(gt = 0, description = "el id ingresado debe ser mayor a cero")):

    for producto in database:
        if producto["id"] == id:
            return producto["nombre"]

    return {"error": "el id no coincide con ningun producto"}


@app.get('/database/nombre/{nombre}') # tengo que poner "/nombre/" en la url porque sino se pisa con el otro get
async def obtener_precio(nombre: str = Path(min_length = 1, description = "el campo no puede estar vacio")):

    for producto in database:
        if producto["nombre"] == nombre:
            return f"el precio por unidad de {nombre} es de {producto['precio']}$"

    return {"error": "el nombre esta mal escrito o el producto no existe"}


@app.post('/database')
async def postear_item(id: int = Body(gt = 0, description = "el id no puede ser menor a cero"),
               nombre: str = Body(min_length = 1, description = "el campo no puede estar vacio"),
               precio: float = Body(gt = 0, description = "no puede ser gratis ni tener precio negativo")):

    for producto in database:
        if producto["nombre"] == nombre:
            return {"error": "el nombre ya esta en uso"}

        elif producto["id"] == id:
            return {"error": "el id ya esta en uso"}
    
    database.append({"id": id,
                     "nombre": nombre,
                     "precio": precio})
    return database


@app.put('/database/{id}')
async def modificar_nombre(id: int = Path(gt = 0, description = "el id debe ser mayor a cero"),
                           nombre: str = Body(min_length = 1, description = "el campo no puede estar vacio")):

    for producto in database:
        if producto["id"] == id and producto["nombre"] == nombre:
            return {"error": "es el mismo nombre que el producto ya tiene"}

        elif producto["nombre"] == nombre:
            return {"error": "otro producto ya tiene ese nombre, seria confuso que lo tuviesen igual, verdad?"}

        elif producto["id"] == id:
            producto["nombre"] = nombre
            return producto

    return {"error": "ningun producto tiene asignado ese id"}


@app.delete('/database/{id}')
async def borrar_item(id: int = Path(gt = 0, description = "el id no puede ser cero o menor a cero"),
                      logico: bool = Query(default = False, description = "borrado fisico permanente?")):

    for producto in database:
        if producto["id"] == id:
            if logico == False:
                producto["activo"] = False
                return {"exito": "producto desactivado"}

            else:
                database.remove(producto)
                return {"exito": "producto borrado permanentemente"}

    return {"error": "el id no cincide con ningun producto existente"}
