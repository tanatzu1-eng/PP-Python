from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


url_sqlite = "sqlite:///./articulos.db"

engine = create_engine(url_sqlite, connect_args = {"check_same_thread": False})

session = sessionmaker(bind = engine, autocommit = False, autoflush = False)


base = declarative_base()


# proveedor de sesiones:
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()