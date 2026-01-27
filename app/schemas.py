from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(min_length = 1, max_length = 100)

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    user_id: int
    title: str = Field(min_length = 1, max_length = 200)

class TaskOut(BaseModel):
    id: int
    user_id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True



    