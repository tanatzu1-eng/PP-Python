from fastapi import FastAPI
from sqlmodel import SQLModel


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Server funcionando"}