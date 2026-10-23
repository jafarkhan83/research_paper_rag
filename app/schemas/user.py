from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str
    k: int
    r: int
    s: int

class UserResponse(BaseModel):
    response: str