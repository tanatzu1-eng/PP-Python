from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import articulo, anidados
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix="/articulos", tags=["articulos"])


@router.get("/", response_model = list[anidados.ArticuloNested])
def database_articulo_completa(db: Session = Depends(get_db)):
    return db.exec(select(articulo.Articulo)).all()


@router.get("/{id}", response_model = anidados.ArticuloNested)
def articulo_database(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    articulo_buscado = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if articulo_buscado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    return articulo_buscado


@router.post("/", response_model = articulo.ArticuloCreate)
def crear_articulo(nuevo_articulo: articulo.ArticuloCreate, db: Session = Depends(get_db)):

    if db.exec(select(articulo.Articulo).where(articulo.Articulo.nombre == nuevo_articulo.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del articulo ya existe")

    db_articulo = articulo.Articulo.model_validate(nuevo_articulo)
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)

    return db_articulo


@router.put("/{id}", response_model = articulo.ArticuloPublic)
def actualizar_articulo(id: PARAMETROS_ID, articulo_actualizado: articulo.ArticuloCreate, db: Session = Depends(get_db)):

    articulo = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if not articulo:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    articulo.nombre = articulo_actualizado.nombre
    articulo.precio = articulo_actualizado.precio
    articulo.disponible = articulo_actualizado.disponible
    articulo.marca = articulo_actualizado.marca

    db.commit()
    db.refresh(articulo)

    return articulo


@router.delete("/{id}", response_model = articulo.ArticuloPublic)
def borrar_articulo(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    articulo = db.exec(select(articulo.Articulo).where(articulo.Articulo.id == id)).first()

    if articulo is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun articulo")

    db.delete(articulo)
    db.commit()

    return articulo
