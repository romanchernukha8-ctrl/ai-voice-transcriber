from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.security.hashing import hash_password


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