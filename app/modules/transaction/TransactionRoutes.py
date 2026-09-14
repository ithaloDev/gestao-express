from fastapi import APIRouter

TransactionRouter = APIRouter(
    prefix="/transaction",
    tags=["transactions"]
)

@TransactionRouter.get("/")
def index():
    return {"Status":"Ativo"}