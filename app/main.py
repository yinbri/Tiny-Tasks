from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tiny Tasks API")

@app.post("/users/", response_model=schemas.UserOut, status_code=201)
def create_user(payload:schemas.UserCreate, db:Session = Depends(get_db)):
    return crud.create_user(db, payload)

@app.get("/users/", response_model=list[schemas.UserOut])
def list_users(db:Session = Depends(get_db)):
    return crud.list_users(db)

@app.delete("/users/{user_id}/", status_code=204)
def delete_user(user_id:int, db:Session = Depends(get_db)):
    try:
        crud.delete_user(db, user_id)
    except ValueError as e:
        if str(e) == "user_not_found":
            raise HTTPException(status_code=404, detail="User not found")
        raise

@app.post("/tasks/", response_model=schemas.TaskOut, status_code=201)
def create_task(payload:schemas.TaskCreate, db:Session = Depends(get_db)):
    try:
        return crud.create_task(db, payload)
    except ValueError as e:
        if str(e) == "user_not_found":
            raise HTTPException(status_code=404, detail="User not found")
        raise


@app.get("/tasks/", response_model=list[schemas.TaskOut])
def list_tasks(db:Session = Depends(get_db)):
    return crud.list_tasks(db)

@app.get("/users/{user_id}/tasks/", response_model=list[schemas.TaskOut])
def list_user_tasks(user_id:int, db:Session = Depends(get_db)):
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.list_user_tasks(db, user_id)
    





