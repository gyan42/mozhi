"""
https://fastapi.tiangolo.com/tutorial/cors/

"""
from typing import Optional
from datetime import datetime, timedelta
import uvicorn
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from api.routers.nlp import nlp
from api.routers.db import db
from api.routers.ner.model import spacy_ner
# from api.routers.ner.model import transformers_ner
# from api.routers.ocr.calamari import calamari
from api.routers.ocr.tesseract import tesseract
from api.routers.storage import minio
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# https://frankie567.github.io/fastapi-users/configuration/full-example/
import databases
import sqlalchemy
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


app = FastAPI(
    # root_path="/api/v1",
    title="Mozhi API Service",
    description="""Visit http://0.0.0.0:8088/docs for the API interface.""",
    version="0.0.1"
)
app.include_router(nlp.router)
app.include_router(db.router)

# app.include_router(calamari.router)
app.include_router(tesseract.router)
app.include_router(spacy_ner.router)
# app.include_router(transformers_ner.router)
app.include_router(minio.router)

ALLOWED_ORIGINS = ["*"]

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root(request: Request):
    return {"message": "Hello, Welcome to Mozhi API.", "root_path": request.scope.get("root_path")}


@app.get("/hw")
def read_main(request: Request):
    return {"message": "Hello World! Mozhi backend responds as expected.", "root_path": request.scope.get("root_path")}


# https://github.com/tiangolo/fastapi/issues/1663
def check_routes(request: Request):
    # Using FastAPI instance
    url_list = [
        route.path
        for route in request.app.routes
        if "rest_of_path" not in route.path
    ]
    # Dump fix for /mozhi/db/text/table/
    if request.url.path not in url_list and '/mozhi/db/text/table/' not in request.url.path:
        return JSONResponse({"detail": request.url.path + " Not Found"}, status.HTTP_404_NOT_FOUND)


# Handle CORS preflight requests
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = check_routes(request)
    if response:
        return response

    response = Response(
        content="OK",
        media_type="text/plain",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
    )
    return response


# Add CORS headers
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = check_routes(request)
    if response:
        return response

    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# -----------------------------------------------------------------------------------------------------

DATABASE_URL = "sqlite:///./test.db"
SECRET = "dc5375c4756902155290c885070a2ae8baa70cdb8aa100d2097de1d9dc2965b6"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
