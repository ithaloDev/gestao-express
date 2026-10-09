from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from typing import Generator

connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, echo=False)

# Função para criar todas as tabelas no banco de dados
def create_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
