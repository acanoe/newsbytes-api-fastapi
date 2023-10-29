from pydantic import BaseModel, constr

from ..schemas import MessageResponse


class UserCredentials(BaseModel):
    username: constr(min_length=3, max_length=20, to_lower=True, strip_whitespace=True)
    password: constr(min_length=3, max_length=20, strip_whitespace=True)


class LoginRequest(UserCredentials):
    pass


class LoginResponse(BaseModel):
    token: str


class RegisterRequest(UserCredentials):
    pass


class RegisterResponse(MessageResponse):
    pass
