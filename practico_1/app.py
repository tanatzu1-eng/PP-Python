from fastapi import FastAPI

app = FastAPI()

'''
@app.get("/")
async def saludar():
    return {"hola": "mundo"}
"""async es un comando de python para que una funcion se pueda ejecutar asincronicamente entre usuarios,
ahora no es necesario usarlo, pero en el mundo profesional, cuando haya mucha gente ejecutando el codigo
si va a ser importante"""

@app.post("/saludo/post")
def post():
    return {"hola": "post"}

@app.put("/saludo/put")
def put():
    return {"hola": "put"}

@app.patch("/saludo/patch")
def path():
    return {"hola": "patch"}

@app.delete("/saludo/delete")
def delete():
    return {"hola": "delete"}
'''





productos = [ # esto es para simular una base de datos
    {"id": 1, "nombre": "producto1", "precio": 1000},
    {"id": 2, "nombre": "producto2", "precio": 2000},
    {"id": 3, "nombre": "producto3", "precio": 3000},
]

@app.get('/')
async def obtener_dato_por_id(id: int):
    for producto in productos:
        if producto['id'] == id:
            return producto
    return{"detalle": "producto no encontrado"}



@app.get('/productos/{id}')
async def obtener_datos_all():
    return productos



@app.post('/')
async def agregar_dato(id: int, nombre: str, precio: float):
    nuevo_producto = {
        "id": id,
        "nombre": nombre,
        "precio": precio
    }

    for producto in productos:
        if nombre == producto["nombre"]:
            return {"error": "ese nombre ya existe"}
        elif id == producto["id"]:
            return {"error": "ese id ya existe"}

    productos.append(nuevo_producto)
    return nuevo_producto



@app.patch('/')
async def alterar_un_dato(id: int, nombre: str, precio: float):
    for producto in productos:
        if id == producto["id"]:
            if nombre == "" and precio != "":
                producto["nombre"] = producto["nombre"]
                producto["precio"] = precio
                return producto
            
            elif precio == "" and nombre != "":
                producto["precio"] = producto["precio"]
                producto["nombre"] = nombre
                return producto
            
            elif precio == "" and nombre == "":
                producto["precio"] = producto["precio"]
                producto["nombre"] = producto["nombre"]
                return producto
            
            elif producto["nombre"] != nombre and producto["precio"] != precio:
                producto["nombre"] = nombre
                producto["precio"] = precio
                return producto



@app.put
async def alterar_datos():
    pass



@app.delete('/')
async def borrar_dato(id: int):
    for producto in productos:
        if id == producto["id"]:
            productos.remove(producto)
            return productos
        if id != producto["id"]:
            return {"error": "no existe un producto con ese id asignado"}
