from fastapi import APIRouter, HTTPException, Path,  Depends

from database import get_db
from sqlalchemy.orm import session
from models import models_articulos
from schemas.schemas_articulos import PARAMETROS_ID, PARAMETROS_NOMBRE, PARAMETROS_PRECIO, PARAMETROS_DISPONIBLE, ArticuloSchema, UpdateSchema


router = APIRouter()


#===================================================================================================================================================
# path operations:
#===================================================================================================================================================
@router.get("/", response_model = list[ArticuloSchema])
def ver_database(db: session = Depends(get_db)):

    return db.query(models_articulos.Articulo).all()


@router.get("/{id}", response_model = ArticuloSchema)
def ver_articulo(id: PARAMETROS_ID, db: session = Depends(get_db)):
    articulo = db.query(models_articulos.Articulo).filter(models_articulos.Articulo.id == id).first() # first() me devuelve solo el primer
    # resultado en caso de haber mas de uno (ahora es innecesario porque estoy filtrando por id, pero si filtrara por nombre o algun parametro
    # repetible necesitaria first)

    if articulo is None:
        raise HTTPException(status_code = 404, detail = "Articulo no encontrado")

    return articulo


@router.post("/", response_model = ArticuloSchema)
def crear_articulo(
    articulo: UpdateSchema,
    db: session = Depends(get_db)):

    nuevo_articulo = models_articulos.Articulo(
        nombre = articulo.nombre,
        precio = articulo.precio,
        disponible = articulo.disponible,
    )

    if db.query(models_articulos.Articulo).filter(models_articulos.Articulo.nombre == articulo.nombre).first():
            raise HTTPException(status_code = 400, detail = "Nombre de articulo ya existente")

    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)
    return nuevo_articulo


@router.put("/{id}", response_model = UpdateSchema)
def editar_articulo(id: PARAMETROS_ID, articulo: UpdateSchema, db: session = Depends(get_db)):
    articulo_editado = db.query(models_articulos.Articulo).filter(models_articulos.Articulo.id == id).first()

    if articulo_editado is None:
        raise HTTPException(status_code = 404, detail = "Id de articulo no encontrado")

    articulo_editado.nombre = articulo.nombre
    articulo_editado.precio = articulo.precio
    articulo_editado.disponible = articulo.disponible

    db.commit()
    db.refresh(articulo_editado)
    return articulo_editado


@router.delete("/{id}", response_model = ArticuloSchema)
def borrar_articulo(id: PARAMETROS_ID, db: session = Depends(get_db)):
    articulo_borrado = db.query(models_articulos.Articulo).filter(models_articulos.Articulo.id == id).first()

    if articulo_borrado is None:
        raise HTTPException(status_code = 404, detail = "Id de articulo no encontrado")

    db.delete(articulo_borrado)
    db.commit()
    return articulo_borrado
#===================================================================================================================================================
