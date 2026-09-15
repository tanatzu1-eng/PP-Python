from fastapi import FastAPI
from .database import base, engine
from .models import models_articulos


base.metadata.create_all(bind = engine)


app = FastAPI()

app.title = "App"