from sqlmodel import SQLModel, Session, create_engine


url = "sqlite://src/practico6_alembic/database.db"

engine = create_engine(url, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session