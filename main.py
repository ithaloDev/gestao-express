import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.routes import routes

# # Inicialização do banco de dados e criação de tabelas
# @asynccontextmanager
# async def init_db(app: FastAPI):
#     # Ligar o banco e cria as tabelas do banco ao ligar o app
#     create_db()
#     yield

app = FastAPI(
    title="Gestão Express",
    description="Uma api para gerenciamento de despesas e controle de gastos"
    )

app.include_router(prefix="/api", router=routes)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)