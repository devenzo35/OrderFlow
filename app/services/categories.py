from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User, Category, Movement
from app.schemas import CategoryCreate, CategoryUpdate
from fastapi import HTTPException, status


async def get_categories_v1(current_user: User, db: AsyncSession) -> list[Category]:
    all_categories = await db.scalars(
        select(Category).filter(Category.user_id == current_user.id)
    )

    if not all_categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No categories found"
        )

    return [category for category in all_categories]


async def get_category_v1(
    category_id: int, db: AsyncSession, current_user: User
) -> Category:
    get_category = await db.scalar(
        select(Category)
        .filter(Category.id == category_id)
        .filter(Category.user_id == current_user.id)
    )

    if not get_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist"
        )

    return get_category


async def create_category_v1(
    category: CategoryCreate,
    db: AsyncSession,
    current_user: User,
):
    # Business rule: The category name must be unique per user.
    exists = await db.scalar(select(Category).filter(Category.name == category.name))

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This category already exist",
        )

    new_category = Category(**category.model_dump(), user_id=current_user.id)

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


async def update_category_v1(
    category: CategoryUpdate,
    category_id: int,
    db: AsyncSession,
    current_user: User,
):
    category_to_update = await db.scalar(
        select(Category)
        .filter(Category.id == category_id)
        .filter(Category.user_id == current_user.id)
    )

    if not category_to_update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This category already exist",
        )

    field_to_update = category.model_dump(exclude_unset=True)

    print(field_to_update)

    for field, value in field_to_update.items():
        setattr(category_to_update, field, value)

    await db.commit()
    await db.refresh(category_to_update)

    return category_to_update


async def delete_category_v1(
    category_id: int,
    db: AsyncSession,
    current_user: User,
):
    category_to_delete = await db.scalar(
        select(Category)
        .filter(Category.id == category_id)
        .filter(Category.user_id == current_user.id)
    )

    if not category_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This category does not exist",
        )

    category_in_use = await db.scalar(
        select(Movement).filter(Movement.category_id == category_id)
    )

    if category_in_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category is being use in movement: {category_in_use.description}",
        )

    await db.delete(category_to_delete)
    await db.commit()

    return category_to_delete
