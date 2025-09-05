from sqlmodel import create_engine, Session
from app.core.config import settings
from typing import Generator

engine = create_engine(str(settings.DATABASE_URI))


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
