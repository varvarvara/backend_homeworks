from fastapi import Depends, FastAPI, status

from app.core.auth import get_current_user
from app.schemas.users import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.users import UserService

app = FastAPI(title="Legacy JWT API")

@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    return await UserService.register_user(user)


@app.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    return await UserService.login_user(user)


@app.get("/protected", status_code=status.HTTP_200_OK)
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "Protected route accessed", "user": current_user["sub"]}
