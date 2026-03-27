from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def saludar():
    return {"hola": "mundo"}

@app.post("/saludo/post")
def post():
    return {"hola": "post"}

@app.put("/saludo/post")
def put():
    return {"hola": "put"}

@app.path("/saludo/path")
def path():
    return {"hola": "path"}

@app.delete("/saludo/delete")
def delete():
    return {"hola": "delete"}