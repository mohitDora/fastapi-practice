from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User


class TodoBase(SQLModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Todo(TodoBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: Optional[datetime] = Field(default=None)
    owner_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

    owner: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoPublic(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner_id: int


class TodosPublic(SQLModel):
    data: list[TodoPublic]
    count: int
