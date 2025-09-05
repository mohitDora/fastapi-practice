# app/crud/todo.py
from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from app.crud.base import CRUDBase
from app.models.todo import Todo, TodoCreate, TodoUpdate


class CRUDTodo(CRUDBase[Todo, TodoCreate, TodoUpdate]):
    def create_with_owner(
        self, session: Session, *, obj_in: TodoCreate, owner_id: int
    ) -> Todo:
        obj_in_data = obj_in.model_dump()
        db_obj = Todo(**obj_in_data, owner_id=owner_id)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self,
        session: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100,
        completed: Optional[bool] = None,
        priority: Optional[str] = None
    ) -> list[Todo]:
        statement = select(Todo).where(Todo.owner_id == owner_id)
        
        if completed is not None:
            statement = statement.where(Todo.is_completed == completed)
        
        if priority:
            statement = statement.where(Todo.priority == priority)
        
        statement = statement.offset(skip).limit(limit).order_by(Todo.created_at.desc())
        return list(session.exec(statement).all())

    def update(
        self, session: Session, *, db_obj: Todo, obj_in: TodoUpdate | dict
    ) -> Todo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        update_data["updated_at"] = datetime.utcnow()
        
        return super().update(session, db_obj=db_obj, obj_in=update_data)

    def get_by_owner(
        self, session: Session, *, id: int, owner_id: int
    ) -> Optional[Todo]:
        statement = select(Todo).where(Todo.id == id, Todo.owner_id == owner_id)
        return session.exec(statement).first()

    def count_by_owner(self, session: Session, *, owner_id: int) -> int:
        statement = select(Todo).where(Todo.owner_id == owner_id)
        return len(list(session.exec(statement).all()))

    def count_completed_by_owner(self, session: Session, *, owner_id: int) -> int:
        statement = select(Todo).where(
            Todo.owner_id == owner_id, Todo.is_completed == True
        )
        return len(list(session.exec(statement).all()))


todo = CRUDTodo(Todo)