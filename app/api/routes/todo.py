from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query

from app.api import deps
from app.crud import todo as crud_todo
from app.models.todo import Todo, TodoCreate, TodoPublic, TodosPublic, TodoUpdate

router = APIRouter()


@router.post("/", response_model=TodoPublic)
def create_todo(
    session: deps.SessionDep, current_user: deps.CurrentUser, todo_data: TodoCreate
) -> Any:
    todo = crud_todo.todo.create_with_owner(session, obj_in=todo_data, owner_id=1)
    return todo


@router.get("/", response_model=TodosPublic)
def read_todos(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
    skip: int = 0,
    limit: int = Query(10, le=100),
    completed: Optional[bool] = None,
) -> Any:
    todos = crud_todo.todo.get_multi_by_owner(
        session, owner_id=current_user.id, skip=skip, limit=limit, completed=completed
    )

    count = crud_todo.todo.count_by_owner(session, owner_id=current_user.id)

    return TodosPublic(
        data=todos,
        count=count,
    )


@router.get("/{todo_id}", response_model=TodoPublic)
def read_todo(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
    todo_id: int,
) -> Any:
    todo = crud_todo.todo.get_by_owner(session, id=todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoPublic)
def update_todo(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
    todo_id: int,
    todo_data: TodoUpdate,
) -> Any:
    todo = crud_todo.todo.get_by_owner(session, id=todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = crud_todo.todo.update(session, db_obj=todo, obj_in=todo_data)
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    session: deps.SessionDep,
    current_user: deps.CurrentUser,
    todo_id: int,
) -> Any:
    todo = crud_todo.todo.get_by_owner(session, id=todo_id, owner_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = crud_todo.todo.remove(session, id=todo_id)
    return todo
