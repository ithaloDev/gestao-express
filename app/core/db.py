from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

connect_args = {"check_same_thread": False}

# Função para criar todas as tabelas no banco de dados
def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            session.rollback()
            session.close()
            raise e

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args, echo=False)