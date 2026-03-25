from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from core.database import get_db
from core.security import hash_password
from schemas import UserRegistrationSchema
from models import User


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, new_user: UserRegistrationSchema):
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = hash_password(new_user.password)
        user_dict.pop("password")
        db_user = User(**user_dict)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user

    async def get_by_email(self, email: str | EmailStr):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


    async def get_by_username(self, username: str):
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
