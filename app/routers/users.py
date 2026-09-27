from schemas.user import UserQuery, UserResponse
from fastapi import APIRouter

router = APIRouter()

@router.get('/hello')
def hello():
    return {"message": "Hello, World!"}

@router.post('/chat')
def chat(body: UserQuery):
    response = UserResponse(response="Hello, World!")
    return response