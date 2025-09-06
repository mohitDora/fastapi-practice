from fastapi import APIRouter

from app.api.routes import auth, todo

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(todo.router, prefix="/todos", tags=["todos"])