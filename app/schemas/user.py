from pydantic import BaseModel

class UserQuery(BaseModel):
    access_token: str
    query: str

class UserResponse(BaseModel):
    response: str