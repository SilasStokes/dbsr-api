
# Api Sample:
# {
#     "oldVal": " At the Party",
#     "newVal": " At the Party asdasd",
#     "changedCol": "Song Title",
#     "row": {
#         "Artist": " At the Party asdasd",
#         "Song Title": "Black Belt Eagle Scout "
#     }
# }
# exterior imports:
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column # ignore
from sqlalchemy.orm import relationship

# local imports
from database import Base


class SongMetadata(Base):
    __tablename__ = "songs"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist: Mapped[Optional[str]]
    def __repr__(self) -> str:
        return f"SongMetadata({self.id=}, {self.title=}, {self.artist=})"

from pydantic import BaseModel
