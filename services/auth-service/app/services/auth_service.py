from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.security.hashing import hash_password
from fastapi import HTTPException, status

from app.schemas import UserLogin, Token
from app.security.hashing import verify_password
from shared.security.jwt import create_access_token


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, user_data: UserCreate) -> User:
        existing_email = await self.repository.get_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already registered")

        existing_username = await self.repository.get_by_username(
            user_data.username
        )
        if existing_username:
            raise ValueError("Username already exists")

        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hash_password(user_data.password),
        )

        return await self.repository.create(user)

    async def login(self, user_data: UserLogin) -> Token:
        user = await self.repository.get_by_email(user_data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(str(user.id))

        return Token(
            access_token=access_token,
            token_type="bearer",
        )