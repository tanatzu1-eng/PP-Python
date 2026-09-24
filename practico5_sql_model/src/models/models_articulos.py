from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class Articulo(Base):
    __tablename__ = "Articulos"

    id = Column(Integer, primary_key = True, index = True)
    nombre = Column(String, index = True)
    precio = Column(Float)
    disponible = Column(Boolean, default = True)