from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas

def create_user(db: Session, payload:schemas.UserCreate) -> models.User:
    user = models.User(name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None:
    user = db.get(models.User, user_id)
    if user is None:
        raise ValueError("user_not_found")
    db.delete(user)
    db.commit()

def list_users(db: Session) -> list[models.User]:
    return list(db.scalars(select(models.User)).all())

def get_user(db:Session, user_id:int) ->models.User | None:
    return db.get(models.User, user_id)

def create_task(db: Session, payload:schemas.TaskCreate) -> models.Task:
    user = get_user(db, payload.user_id)

    if user is None:
        raise ValueError("user_not_found")
    
    task = models.Task(
        user_id = payload.user_id,
        title = payload.title,
        completed = False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task
    
def list_tasks(db: Session) -> list[models.Task]:
    return list(db.scalars(select(models.Task)).all())

def list_user_tasks(db: Session, user_id:int) -> list[models.Task]:
    stmt = select(models.Task).where(models.Task.user_id == user_id)
    return list(db.scalars(stmt).all())
