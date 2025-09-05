from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.todo import Todo


class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    todos: list["Todo"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    password: str


class UserRegister(SQLModel):
    pass


class UserUpdate(UserBase):
    email: Optional[str] = None  # type: ignore
    password: Optional[str] = None


class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
