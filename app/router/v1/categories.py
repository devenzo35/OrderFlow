from fastapi import APIRouter, status, Depends
from app.models import User
from app.schemas import CategoryCreate, CategoryPublic, CategoryUpdate
from app.services.categories import (
    create_category_v1,
    delete_category_v1,
    get_categories_v1,
    get_category_v1,
    update_category_v1,
)
from ...dependencies import get_db, get_current_user
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories V1"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


@router.get("/", response_model=list[CategoryPublic])
async def get_categories(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return await get_categories_v1(current_user, db)


@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_category_v1(
        category_id=category_id, db=db, current_user=current_user
    )


@router.post("/", response_model=CategoryCreate)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await create_category_v1(category, db, current_user)


@router.patch("/{category_id}")
async def update_category(
    category: CategoryUpdate,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return await update_category_v1(category, category_id, db, current_user)


@router.delete("/{category_id}", response_model=CategoryPublic)
async def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_category_v1(category_id, db, current_user)
