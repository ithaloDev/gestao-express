from fastapi import APIRouter
from .modules.transaction.TransactionRoutes import TransactionRouter

routes = APIRouter()

routes.include_router(TransactionRouter)