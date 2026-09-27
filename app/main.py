from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from routers.users import router as user_router
from routers.auth import router as auth_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dependencies.database import engine, Base

app = FastAPI()

# database setup
# Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(user_router)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "response": "Invalid request body"
        }
    )

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "response": exc.detail
        }
    )

@app.exception_handler(Exception)
def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "response": "Internal server error"
        }
    )