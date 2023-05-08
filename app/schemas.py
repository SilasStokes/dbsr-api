from pydantic import BaseModel, Field



# models.py: SQLAlchemy models
# schemas.py: Pydantic models

# Prepending meaning:
# GS: are for interacting with Google Sheets
# DBSR: are for interacting with the DBSR Flight Deck Electron App. 
# PG: Interacting with Postgres database

# Google sheet classes:
class GSEditRow(BaseModel):
    artist: str = Field(alias='Artist')
    song_title: str = Field(alias='Song Title')
    id: int

    class Config:
        allow_population_by_field_name = True


class GSEdit(BaseModel):
    old_val: str = Field(alias='oldVal')
    new_val: str = Field(alias='newVal')
    changed_col: str = Field(alias='changedCol')
    row: GSEditRow
    
    class Config:
        allow_population_by_field_name = True
        


class DBSRDroppedFiles(BaseModel):
    file_paths: list[str]
    
# need to add stripping to remove the validation
class Metadata(BaseModel):
    artist : str | None
    title : str | None
    acoustid : str | None
    album : str | None
    album_artist : str | None
    path: str
    

class PotentialMetadatas(BaseModel):
    filename : str
    type: str
    potentialMetadata : list[Metadata | None ]

class ReturnType(BaseModel):
    error: str = ''
    results: list[PotentialMetadatas] = []