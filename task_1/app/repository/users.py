from pydantic import EmailStr
from sqlalchemy import select

from app.core.db import SessionLocal
from app.schemas.users import UserCreate
from app.models import User


class UserRepository:
    @classmethod
    async def create_one(cls, data: UserCreate, hashed_password: str) -> User:
        async with SessionLocal() as session:
            user_dict = data.model_dump(exclude={"password"})
            user_dict["hashed_password"] = hashed_password
            db_user = User(**user_dict)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    @classmethod
    async def get_by_email(cls, email: str | EmailStr) -> User | None:
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_username(cls, username: str) -> User | None:
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, user_id: int) -> User | None:
        async with SessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
