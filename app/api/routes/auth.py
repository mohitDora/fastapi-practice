from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import SQLModel
from datetime import timedelta

from app.api import deps
from app.models.user import UserLogin, UserRegister
from app.crud import user as crud_user
from app.core.config import settings
from app.core import security


class Token(SQLModel):
    access_token: str
    token_type: str


class Messsge(SQLModel):
    message: str


router = APIRouter()


@router.post("/login")
def login(session: deps.SessionDep, user_data: UserLogin) -> Token:
    user = crud_user.user.authenticate(
        session, email=user_data.email, password=user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not crud_user.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return Token(
        access_token=security.create_token(user.id, expires_delta=access_token_expires),
        token_type="bearer",
    )


@router.post("/register")
def register(session: deps.SessionDep, user_data: UserRegister):
    user = crud_user.user.get_by_email(session, email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_create = crud_user.UserCreate.model_validate(user_data)
    user = crud_user.user.create(session, obj_in=user_create)
    return user


@router.get("/test")
def testToken(current_user: deps.CurrentUserDep):
    return current_user
