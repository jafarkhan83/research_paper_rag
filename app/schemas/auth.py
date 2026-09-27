from pydantic import BaseModel

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

    def __str__(self):
        return f"RegisterRequest(name={self.name}, email={self.email})"

class LoginRequest(BaseModel):
    email: str
    password: str

    def __str__(self):
        return f"LoginRequest(email={self.email})"

class TokenResponse(BaseModel):
    response: str