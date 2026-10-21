from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str

class UserResponse(BaseModel):
    response: str