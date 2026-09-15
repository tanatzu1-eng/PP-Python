from ..database import base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Articulo(base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String, index = True)
    precio = Column(Float)
    disponible = Column(Boolean, default = True)