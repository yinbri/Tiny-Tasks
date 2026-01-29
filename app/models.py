from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(200), nullable=True, unique=True)


    tasks: Mapped[list["Task"]] = relationship(back_populates = "user")

class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable = False)

    title:Mapped[str] = mapped_column(String(200), nullable = False)
    completed:Mapped[bool] = mapped_column(Boolean, nullable = False, default = False)

    user: Mapped["User"] = relationship(back_populates = "tasks")