from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ..database import get_db

from ..models import proveedor, anidados
from ..schemas.esquemas import PARAMETROS_ID


router = APIRouter(prefix="/proveedores", tags=["proveedores"])


@router.get("/", response_model = list[anidados.ProveedorNested])
def database_proveedor_completa(db: Session = Depends(get_db)):
    return db.exec(select(proveedor.Proveedor)).all()


@router.get("/{id}", response_model = anidados.ProveedorNested)
def proveedor_database(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    resultado = db.exec(select(proveedor.Proveedor).where(proveedor.Proveedor.id == id)).first()

    if resultado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con el de ningun proveedor")

    return resultado


@router.post("/", response_model = proveedor.ProveedorCreate)
def crear_proveedor(nuevo_proveedor: proveedor.ProveedorCreate, db: Session = Depends(get_db)):

    if db.exec(select(proveedor.Proveedor).where(proveedor.Proveedor.nombre == nuevo_proveedor.nombre)).first():
        raise HTTPException(status_code = 400, detail = "el nombre del proveedor ya existe")

    db_proveedor = proveedor.ProveedorPublic.model_validate(nuevo_proveedor)
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)

    return db_proveedor


@router.put("/{id}", response_model = proveedor.ProveedorPublic)
def actualizar_proveedor(id: PARAMETROS_ID, proveedor_actualizado: proveedor.ProveedorCreate, db: Session = Depends(get_db)):

    resultado = db.exec(select(proveedor.Proveedor).where(proveedor.Proveedor.id == id)).first()

    if not resultado:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun proveedor")

    resultado.nombre = proveedor_actualizado.nombre
    resultado.precio = proveedor_actualizado.precio
    resultado.disponible = proveedor_actualizado.disponible
    resultado.marca = proveedor_actualizado.marca

    db.commit()
    db.refresh(resultado)

    return resultado


@router.delete("/{id}", response_model = proveedor.ProveedorPublic)
def borrar_proveedor(id: PARAMETROS_ID, db: Session = Depends(get_db)):

    resultado = db.exec(select(proveedor.Proveedor).where(proveedor.Proveedor.id == id)).first()

    if resultado is None:
        raise HTTPException(status_code = 404, detail = "el id no coincide con ningun proveedor")

    db.delete(resultado)
    db.commit()

    return resultado
