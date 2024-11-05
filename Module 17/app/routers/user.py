from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from app.models import *
from app.schemas import CreateUser, UpdateUser
from app.backend.db_depends import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete

from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users


# @router.put("/update2")
# async def update_user_2(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
#     user_ = db.query(User).filter(User.id == user_id).first()
#     if user_ is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="There is no user found"
#         )
#     else:
#         return "ffff"

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_ = db.query(User).filter(User.id == user_id).first()
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    else:
        return user_


@router.post("/create")
async def create_user_(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username, firstname=create_user.firstname,
                                   lastname=create_user.lastname, age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful"
    }


@router.put("/update")
async def update_user_(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user_ = db.query(User).filter(User.id == user_id).first()
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )

    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        firstname=update_user.firstname, lastname=update_user.lastname,
        age=update_user.age, slug=slugify(update_user.username)
    ))

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User update is successful"
    }


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )

    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "User delete is successful"
    }

@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).first()
    if tasks is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks were not found"
        )
    else:
        return tasks
