from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from ..database import get_db

from ..models import modelos
from ..schemas.esquemas import PARAMETROS_ID, PARAMETROS_NOMBRE, PARAMETROS_PRECIO, PARAMETROS_DISPONIBLE


router = APIRouter()


@router.get("/", response_model = list[modelos.ArticuloPublic])
def database_completa(db: Session = Depends(get_db)):
    return db.exec(select(modelos.Articulo)).all()


@router.get("/{id}", response_model = modelos.ArticuloPublic)
def articulo_database(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    articulo = db.exec(select(modelos.Articulo).where(modelos.Articulo.id == id)).first()

    if articulo is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    return articulo


@router.post("/", response_model = modelos.ArticuloCreate)
def crear_articulo(nuevo_articulo: modelos.Articulo, db: Session = Depends(get_db)):

    if db.exec(select(modelos.Articulo).where(modelos.Articulo.nombre == nuevo_articulo.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del articulo ya existe")

    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)

    return nuevo_articulo


@router.put("/{id}", response_model = modelos.ArticuloPublic)
def actualizar_articulo(id: PARAMETROS_ID, articulo_actualizado: modelos.ArticuloCreate, db: Session = Depends(get_db)):

    articulo = db.exec(select(modelos.Articulo).where(modelos.Articulo.id == id)).first()

    if not articulo:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    articulo.nombre = articulo_actualizado.nombre
    articulo.precio = articulo_actualizado.precio
    articulo.disponible = articulo_actualizado.disponible

    db.commit()
    db.refresh(articulo)

    return articulo


@router.delete("/{id}", response_model = modelos.ArticuloPublic)
def borrar_articulo(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    articulo = db.exec(select(modelos.Articulo).where(modelos.Articulo.id == id)).first()

    if articulo is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    db.delete(articulo)
    db.commit()

    return articulo
