from schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies.database import get_db

router = APIRouter()

@router.post("/register")
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    user = User()
    user.name = body.name
    user.email = body.email
    user.password = body.password

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        return JSONResponse(
            status_code=409,
            content= {"response": "email already exists"}
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content= {"response": f"register failed: {str(e)}"}
        )

    return {"response": "register successful"}

@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    # password need to be hashed first then compare

    if not user:
        return JSONResponse(
            status_code=404,
            content= {"response": "invalid email, password pair"}
        )

    token = TokenResponse(response="some_token")
    return token

@router.post("/logout")
def logout():
    return {"response": "Logout successful"}
