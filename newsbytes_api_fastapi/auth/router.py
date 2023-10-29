from typing import Union

from fastapi import APIRouter

from ..schemas import ErrorResponse
from .schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from .utils import create_token, hash_password, verify_password

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=Union[LoginResponse, ErrorResponse])
def login(credentials: LoginRequest):
    data = {
        "username": "test",
        "password": "$2b$12$Q20.Bl97FNTAZlKHzmkuo.zC1JM458fpNkjwpIKl0S903MtdpET2u",
    }

    USERNAME_CORRECT = credentials.username == data["username"]
    PASSWORD_CORRECT = verify_password(credentials.password, data["password"])

    if not (USERNAME_CORRECT and PASSWORD_CORRECT):
        return ErrorResponse(error="Incorrect username or password")

    return LoginResponse(token=create_token(1))


@auth_router.post("/register", response_model=RegisterResponse)
def register(credentials: RegisterRequest):
    user = {
        "username": credentials.username,
        "password": hash_password(credentials.password),
    }
    print(user)
    return RegisterResponse(message="User registered")
