# exterior imports:
from typing import Optional
# from sqlalchemy import ForeignKey
# from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship

# local imports
from .database import Base

# models.py: SQLAlchemy models
# schemas.py: Pydantic models



# SQLAlchemy class
# TODO: Come up with schema for the database
# TODO: Expand to hold all relevant metadata fields
class SQLSongMetadata(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[Optional[str]]
    def __repr__(self) -> str:
        return f"SongMetadata({self.id=}, {self.title=}, {self.artist=})"