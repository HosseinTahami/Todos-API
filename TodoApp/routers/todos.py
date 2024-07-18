from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..database import SessionLocal
from ..models import Todos
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(prefix="/todo", tags=["Todos"])


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=128)
    priority: int = Field(gt=0, le=6)
    complete: bool


def get_db():

    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


# Dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    todo_models = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    return todo_models


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!")


@router.post("/")
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!"
        )

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(ge=1)
):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed."
        )
    todo_model = (
        db.query(Todos)
        .filter(todo_id == Todos.id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found!"
        )
    db.query(Todos).filter(todo_id == Todos.id).filter(
        Todos.owner_id == user.get("id")
    ).delete()
    db.commit()
