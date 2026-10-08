from sqlmodel import create_engine, Session, SQLModel


url_sqlite = "sqlite:///./articulos_sqlmodel.db"

engine = create_engine(url_sqlite, connect_args = {"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session