from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


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