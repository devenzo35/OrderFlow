from fastapi import APIRouter, status, Depends, HTTPException
from ..models.category import Category
from ..models.user import User
from ..schemas.categories import CategoryCreate
from ..dependencies import get_db
from ..router.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"message": status.HTTP_404_NOT_FOUND}},
)

# crear categorias y movimientos


@router.post("/", response_model=CategoryCreate)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    exists = db.query(Category).filter(Category.name == category.name).first()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This category already exist",
        )

    new_category = Category(**category.model_dump(), user_id=current_user.id)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category
