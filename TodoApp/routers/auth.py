from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from ..database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

# JWT Requirements
SECRETE_KEY = "bbe417cd0bbd47e59ea4df5fe5c2d7a8eb0b3bde4c7b68bba87d9024c0d3ea63"
ALGORITHM = "HS256"

# CryptContext Instance
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


def get_db():

    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
token_dependency = Annotated[str, Depends(OAuth2PasswordBearer("auth/token"))]
form_data_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_user(username: str, password: str, db):

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user


def create_access_token(user: CreateUserRequest, expires_delta: timedelta):

    encode = {
        "sub": user.username,
        "id": user.id,
        "exp": datetime.now() + expires_delta,
        "role": user.role,
    }

    return jwt.encode(encode, SECRETE_KEY, algorithm=ALGORITHM)


async def get_current_user(token: token_dependency):

    try:

        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )

        return {
            "username": username,
            "id": user_id,
            "role": user_role,
        }

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    user_model = Users(
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        email=create_user_request.email,
        username=create_user_request.username,
        role=create_user_request.role,
        is_active=True,
        phone_number=create_user_request.phone_number,
    )
    db.add(user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: form_data_dependency, db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    token = create_access_token(user, timedelta(minutes=20))

    return {
        "access_token": token,
        "token_type": "bearer",
    }
