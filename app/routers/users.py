from schemas.user import UserQuery, UserResponse
from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user

router = APIRouter()

@router.get('/hello')
def hello():
    return {"message": "Hello, World!"}

@router.post('/chat')
def chat(body: UserQuery, current_user=Depends(get_current_user)):
    query = body.query
    response = UserResponse(response=f"Hello, {current_user.name}! You said: {query}")
    return response