from pydantic import BaseModel


class LoginResponse(BaseModel):
    token: str

class RegisterResponse(BaseModel):
    message: str