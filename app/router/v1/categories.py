from fastapi import APIRouter, Request, status, Depends
from app.models import User
from app.schemas import CategoryCreate, CategoryPublic, CategoryUpdate
from app.services.categories import (
    create_category_v1,
    delete_category_v1,
    get_categories_v1,
    get_category_v1,
    update_category_v1,
)
from ...dependencies import get_db, get_current_user, default_limiter  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories V1"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)


@router.get("/", response_model=list[CategoryPublic])
@default_limiter  # type: ignore
async def get_categories(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
):
    return await get_categories_v1(current_user, db)


@router.get("/{category_id}", response_model=CategoryPublic)
@default_limiter  # type: ignore
async def get_category(
    request: Request,
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_category_v1(
        category_id=category_id, db=db, current_user=current_user
    )


@router.post("/", response_model=CategoryCreate)
@default_limiter  # type: ignore
async def create_category(
    request: Request,
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await create_category_v1(category, db, current_user)


@router.patch("/{category_id}")
@default_limiter  # type: ignore
async def update_category(
    request: Request,
    category: CategoryUpdate,
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_category_v1(category, category_id, db, current_user)


@router.delete("/{category_id}", response_model=CategoryPublic)
@default_limiter  # type: ignore
async def delete_category(
    request: Request,
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await delete_category_v1(category_id, db, current_user)
