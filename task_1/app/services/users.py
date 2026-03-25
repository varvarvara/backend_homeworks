from app.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from app.core.security import create_access_token, hash_password, verify_password
from app.repository.users import UserRepository
from app.schemas.users import TokenResponse, UserCreate, UserLogin, UserResponse


class UserService:
    @classmethod
    async def register_user(cls, data: UserCreate) -> UserResponse:
        if await UserRepository.get_by_email(data.email):
            raise UserAlreadyExistsException("email", str(data.email))
        if await UserRepository.get_by_username(data.username):
            raise UserAlreadyExistsException("username", data.username)

        user = await UserRepository.create_one(data, hash_password(data.password))
        return UserResponse.model_validate(user, from_attributes=True)

    @classmethod
    async def login_user(cls, data: UserLogin) -> TokenResponse:
        user = await UserRepository.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsException()

        token = create_access_token({"sub": str(user.id), "email": user.email})
        return TokenResponse(access_token=token)

    @classmethod
    async def get_me(cls, user_id: int) -> UserResponse | None:
        user = await UserRepository.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user, from_attributes=True)
