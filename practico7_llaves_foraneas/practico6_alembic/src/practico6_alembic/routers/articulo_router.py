from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import articulo
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix="/articulos", tags=["articulos"])


@router.get("/", response_model = list[articulo.ArticuloPublic])
def database_articulo_completa(db: Session = Depends(get_db)):
    return db.exec(select(articulo.Articulo)).all()


@router.get("/{id}", response_model = articulo.ArticuloPublic)
def articulo_database(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    resultado = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if resultado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    return resultado


@router.post("/", response_model = articulo.ArticuloCreate)
def crear_articulo(nuevo_articulo: articulo.Articulo, db: Session = Depends(get_db)):

    if db.exec(select(articulo.Articulo).where(articulo.Articulo.nombre == nuevo_articulo.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del articulo ya existe")

    db.add(nuevo_articulo)
    db.commit()
    db.refresh(nuevo_articulo)

    return nuevo_articulo


@router.put("/{id}", response_model = articulo.ArticuloPublic)
def actualizar_articulo(id: PARAMETROS_ID, articulo_actualizado: articulo.ArticuloCreate, db: Session = Depends(get_db)):

    resultado = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if not resultado:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    resultado.nombre = articulo_actualizado.nombre
    resultado.precio = articulo_actualizado.precio
    resultado.disponible = articulo_actualizado.disponible
    resultado.marca = articulo_actualizado.marca

    db.commit()
    db.refresh(resultado)

    return resultado


@router.delete("/{id}", response_model = articulo.ArticuloPublic)
def borrar_articulo(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    resultado = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if resultado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    db.delete(resultado)
    db.commit()

    return resultado
