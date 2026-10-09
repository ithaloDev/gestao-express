from fastapi import APIRouter
from app.modules.transactions.routes.TransactionRouter import TransactionRouter
from app.modules.transactions.routes.CategoryRouter import CategoryRouter

routes = APIRouter()

routes.include_router(TransactionRouter)
routes.include_router(CategoryRouter)