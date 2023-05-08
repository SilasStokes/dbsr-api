from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Session 
from .config import settings
# from .models import SQLSongMetadata


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# exterior imports:
from typing import Optional
# from sqlalchemy import ForeignKey
# from sqlalchemy import Column, Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

# local imports
# from .database import Base

# models.py: SQLAlchemy models
# schemas.py: Pydantic models


# Base = declarative_base()
class Base(DeclarativeBase):
    pass
# SQLAlchemy class
# TODO: Come up with schema for the database
# TODO: Expand to hold all relevant metadata fields
class SQLSongMetadata(Base):
    __tablename__ = "songs"
    # id = Column(Integer, primary_key = True)
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[Optional[str]]
    def __repr__(self) -> str:
        return f"SongMetadata({self.id=}, {self.title=}, {self.artist=})"
    
Base.metadata.create_all(engine)

# documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/
# This may have changed: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
