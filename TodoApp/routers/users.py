from fastapi import Depends, APIRouter, status, HTTPException, Body
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
#from passlib.context import CryptContext
from ..models import Users
from pydantic import BaseModel, Field
import bcrypt

router = APIRouter(prefix="/users", tags=["Users"])


class ResetPassword(BaseModel):
    old_password: str
    new_password: str = Field(min_length=3)


class ChangePhoneNumber(BaseModel):
    phone_number: str = Field(max_length=11, min_length=11)


def get_db():

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# CryptContext Instance
#bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/profile", status_code=status.HTTP_200_OK)
async def current_user_info(db: db_dependency, user: user_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    return user_model


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, passwords: ResetPassword
):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt.verify(passwords.old_password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password"
        )

    user_model.hashed_password = bcrypt.hashpw(passwords.new_password)

    db.add(user_model)
    db.commit()


@router.put("/PhoneNumber", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency,
    db: db_dependency,
    phone_number_request: ChangePhoneNumber,
#  phone_number: str = Body()    
):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number_request.phone_number

    db.add(user_model)
    db.commit()
