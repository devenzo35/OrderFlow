from fastapi import status, HTTPException
from app.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_users_v1(db: AsyncSession):
    users = await db.scalars(select(User))

    return [user for user in users]


async def get_user_v1(user_id: int, db: AsyncSession):
    user = await db.scalar(select(User).filter(User.id == user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    return user
