from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
