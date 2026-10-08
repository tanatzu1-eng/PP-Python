from fastapi import APIRouter, HTTPException, Path,  Depends
from sqlmodel import Session, select

from ..database import get_db
from ..models import models_articulos
from ..schemas.schemas_articulos import PARAMETROS_ID, PARAMETROS_NOMBRE, PARAMETROS_PRECIO, PARAMETROS_DISPONIBLE, ArticuloSchema, UpdateSchema


router = APIRouter()


#===================================================================================================================================================
# path operations:
#===================================================================================================================================================
@router.get("/", response_model = list[models_articulos.ArticuloPublic])
def ver_database(db: Session = Depends(get_db)):

    return db.exec(select(models_articulos.Articulo)).all()


@router.get("/{id}", response_model = models_articulos.ArticuloPublic)
def ver_articulo(id: PARAMETROS_ID, db: Session = Depends(get_db)):
    articulo = db.get(models_articulos.Articulo, id)

    if articulo is None:
        raise HTTPException(status_code = 404, detail = "Articulo no encontrado")

    return articulo


@router.post("/", response_model = models_articulos.ArticuloCreate)
def crear_articulo(
    articulo: models_articulos.ArticuloCreate,
    db: Session = Depends(get_db)):

    nuevo_articulo = models_articulos.Articulo.model_validate(articulo)

    if db.query(models_articulos.Articulo).filter(models_articulos.Articulo.nombre == articulo.nombre).first():
                raise HTTPException(status_code = 400, detail = "Nombre de articulo ya existente")
    if db.query(models_articulos.Articulo).filter(models_articulos.Articulo.id == articulo.id).first():
            raise HTTPException(status_code = 400, detail = "Id de articulo ya existente")

    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)
    return nuevo_articulo


@router.put("/{id}", response_model = models_articulos.ArticuloCreate)
def editar_articulo(id: PARAMETROS_ID, articulo: UpdateSchema, db: Session = Depends(get_db)):
    articulo_editado = db.get(models_articulos.Articulo, id)

    if articulo_editado is None:
        raise HTTPException(status_code = 404, detail = "Id de articulo no encontrado")

    articulo_editado.nombre = articulo.nombre
    articulo_editado.precio = articulo.precio
    articulo_editado.disponible = articulo.disponible

    db.commit()
    db.refresh(articulo_editado)
    return articulo_editado


@router.delete("/{id}", response_model = models_articulos.ArticuloCreate)
def borrar_articulo(id: PARAMETROS_ID, db: Session = Depends(get_db)):
    articulo_borrado = db.get(models_articulos.Articulo, id)

    if articulo_borrado is None:
        raise HTTPException(status_code = 404, detail = "Id de articulo no encontrado")

    db.delete(articulo_borrado)
    db.commit()
    return db.exec(select(models_articulos.Articulo)).all()
#===================================================================================================================================================
