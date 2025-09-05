from typing import Optional
from app.models.user import User, UserCreate, UserUpdate
from app.crud.base import CRUDBase
from sqlmodel import Session, select
from app.core.security import get_hash_password, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, session: Session, *, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    def create(self, session: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.model_dump()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_hash_password(obj_in.password)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self, session: Session, *, db_obj: User, obj_in: UserUpdate | dict
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_hash_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(session, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, session: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
