from fastapi import APIRouter

from .schemas import LoginResponse, RegisterResponse

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=LoginResponse)
def login():
    return LoginResponse(token="token")

@auth_router.post("/register", response_model=RegisterResponse)
def register():
    return RegisterResponse(message="User registered")