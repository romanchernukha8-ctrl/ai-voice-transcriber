import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import UserLogin, UserCreate
from app.services.auth_service import AuthService
from app.security.hashing import hash_password
from shared.security.jwt import verify_access_token


class FakeUserRepository:
    async def get_by_email(self, email):
        return None


class FakeUser:
    id = 1
    email = "user@example.com"
    password_hash = hash_password("correct-password")


class FakeUserRepositoryWithUser:
    async def get_by_email(self, email):
        return FakeUser()


class FakeUserRepositoryForRegister:
    def __init__(self):
        self.created_user = None

    async def get_by_email(self, email):
        return None

    async def get_by_username(self, username):
        return None

    async def create(self, user):
        user.id = 1
        self.created_user = user
        return user


class FakeUserRepositoryWithExistingEmail:
    async def get_by_email(self, email):
        return FakeUser()

    async def get_by_username(self, username):
        return None

    async def create(self, user):
        raise AssertionError("create() must not be called")


class FakeUserRepositoryWithExistingUsername:
    async def get_by_email(self, email):
        return None

    async def get_by_username(self, username):
        return FakeUser()

    async def create(self, user):
        raise AssertionError("create() must not be called")


@pytest.mark.anyio
async def test_login_unknown_email():
    repository = FakeUserRepository()
    service = AuthService(repository)

    user_data = UserLogin(
        email="unknown@example.com",
        password="password123",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.login(user_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"


@pytest.mark.anyio
async def test_login_wrong_password():
    repository = FakeUserRepositoryWithUser()
    service = AuthService(repository)

    user_data = UserLogin(
        email="user@example.com",
        password="wrong-password",
    )

    with pytest.raises(HTTPException) as exc_info:
        await service.login(user_data)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid email or password"


@pytest.mark.anyio
async def test_login_success():
    repository = FakeUserRepositoryWithUser()
    service = AuthService(repository)

    user_data = UserLogin(
        email="user@example.com",
        password="correct-password",
    )

    result = await service.login(user_data)

    assert result.access_token
    assert result.token_type == "bearer"

    payload = verify_access_token(result.access_token)

    assert payload["sub"] == "1"
    assert "exp" in payload


@pytest.mark.anyio
async def test_register_success():
    repository = FakeUserRepositoryForRegister()
    service = AuthService(repository)

    user_data = UserCreate(
        email="new@example.com",
        username="newuser",
        password="password123",
    )

    result = await service.register(user_data)

    assert result.id == 1
    assert result.email == "new@example.com"
    assert result.username == "newuser"
    assert result.password_hash != "password123"
    assert repository.created_user is result


@pytest.mark.anyio
async def test_register_duplicate_email():
    repository = FakeUserRepositoryWithExistingEmail()
    service = AuthService(repository)

    user_data = UserCreate(
        email="user@example.com",
        username="newuser",
        password="password123",
    )

    with pytest.raises(ValueError) as exc_info:
        await service.register(user_data)

    assert str(exc_info.value) == "Email already registered"


@pytest.mark.anyio
async def test_register_duplicate_username():
    repository = FakeUserRepositoryWithExistingUsername()
    service = AuthService(repository)

    user_data = UserCreate(
        email="new@example.com",
        username="user",
        password="password123",
    )

    with pytest.raises(ValueError) as exc_info:
        await service.register(user_data)

    assert str(exc_info.value) == "Username already exists"


def test_me_without_token():
    client = TestClient(app)

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_with_invalid_token():
    client = TestClient(app)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )

    assert response.status_code == 401