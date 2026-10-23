from schemas.user import UserQuery, UserResponse
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies.auth import get_current_user
from services.chat_service import ChatService
from functools import lru_cache

router = APIRouter()

@router.get('/hello')
def hello():
    return {"message": "Hello, World!"}

@lru_cache
def get_service():
    return ChatService()

@router.post('/chat')
def chat(body: UserQuery, current_user=Depends(get_current_user), chat_service=Depends(get_service)):
    query = body.query
    try:
        new_query = chat_service.answer(query=query, k=body.k, s=body.s, r=body.r)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    response = UserResponse(response=new_query)
    return response

@router.get('/initialize')
def initialize(current_user=Depends(get_current_user), chat_service=Depends(get_service)):
    try:
        chat_service.initializer()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    return {"message": "Initialization complete!"}