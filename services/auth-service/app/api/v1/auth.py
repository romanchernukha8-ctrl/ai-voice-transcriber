from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.schemas import UserLogin, Token
from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post(
    "/login",
    response_model=Token,
    summary="User login",
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    return await service.login(user)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current user",
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        created_user = await service.register(user)
        return created_user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )