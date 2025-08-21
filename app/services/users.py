from fastapi import status, HTTPException
from app.models import User
from sqlalchemy.orm import Session


async def get_users_v1(db: Session):
    users = db.query(User).all()
    return [user for user in users]


async def get_user_v1(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return user
