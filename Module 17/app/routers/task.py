from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from app.models import *
from app.schemas import CreateTask, UpdateTask
from app.backend.db_depends import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete

from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.query(Task).all()
    return tasks


@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_ = db.query(Task).filter(Task.id == task_id).first()
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        return task_


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user_ = db.query(User).filter(User.id == user_id).first()
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(insert(Task).values(title=create_task.title, content=create_task.content,
                                       priority=create_task.priority, user_id=user_.id,
                                       slug=slugify(create_task.title)))
        db.commit()
        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Successful"
        }


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task_ = db.query(Task).filter(Task.id == task_id).first()
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no user found"
        )

    db.execute(update(User).where(User.id == task_id).values(
        username=update_task.username,
        firstname=update_task.firstname, lastname=update_task.lastname,
        age=update_task.age, slug=slugify(update_task.username)
    ))

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task update is successful"
    }


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no task found"
        )

    db.execute(delete(Task).where(Task.id == task_id))

    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Task delete is successful"
    }

