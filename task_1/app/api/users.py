from fastapi import APIRouter, status

from app.schemas.users import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.users import UserService

userRouter = APIRouter(prefix="/auth", tags=["Auth"])

@userRouter.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    return await UserService.register_user(user)

@userRouter.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    return await UserService.login_user(user)
