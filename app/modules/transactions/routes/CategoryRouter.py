from uuid import UUID
from typing import Sequence
from fastapi import APIRouter, Depends, status
from app.modules.dependencies import get_category_service
from app.modules.transactions.service import CategoryService

from app.modules.transactions.schema import (
    CategoryResponse, 
    CategoryWithTransactionsResponse, 
    DeleteAllResponse
)

CategoryRouter = APIRouter(prefix="/transactions/category", tags=["Categories"])

@CategoryRouter.get("/all", response_model=Sequence[CategoryResponse])
def get_all_categories(service: CategoryService = Depends(get_category_service)):
    return service.get_all()

@CategoryRouter.get("/{category_id}", response_model=CategoryWithTransactionsResponse)
def get_category_by_id(category_id: UUID, service: CategoryService = Depends(get_category_service)):
    return service.get_by_id(category_id)

@CategoryRouter.delete("/all", response_model=DeleteAllResponse, status_code=status.HTTP_200_OK)
def delete_all_unused_categories(service: CategoryService = Depends(get_category_service)):
    return service.delete_all_unused()

@CategoryRouter.delete("/{category_id}", response_model=DeleteAllResponse, status_code=status.HTTP_200_OK)
def delete_category_by_id(category_id: UUID, service: CategoryService = Depends(get_category_service)):
    return service.delete_category(category_id)
