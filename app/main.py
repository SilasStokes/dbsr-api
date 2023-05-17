import os
from typing import Any

# fastapi 
from fastapi import FastAPI, Body, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

import json
import pprint



# relative imports
from .helper import (
        add_file_to_musiclib, 
        generate_acoustid, 
        read_files_from_directory, 
        find_potential_metadata,
        write_metadata_to_file
    )
from .global_vars import MUSIC_FILE_EXTENSIONS
from .config import settings
from .database import get_db, SQLSongMetadata
# from .models import SongMetadata
from .schemas import *
# from .models import *

# needed for sending to gsheets:
# pyright: reportMissingTypeStubs=false
import gspread

# logger set up:
from .log import get_logger
LOG = get_logger(__name__)
LOG.debug("a debug message")
# pp = pprint.PrettyPrinter(indent=4)

## program start:
app = FastAPI()


class Test(BaseModel):
    test: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/edit")
async def onRowEdit(edit: GSEdit, db: Session = Depends(get_db)):

    print(f'onRowEdit Called: {edit=}')

    changed_col_mapping = {
        'Song Title': 'title',
        'Artist': 'artist'
    }
    key = changed_col_mapping[edit.changed_col]
    query = db.query(SQLSongMetadata).filter(SQLSongMetadata.id == edit.row.id)

    # if we don't want to use the id, we can use other fields with the & symbol
    # The parens are essential bc they set the order of operations.
    # query = db.query(SongMetadata).filter(
    #     (SongMetadata.artist == edit.row.artist) & (
    #         SongMetadata.title == edit.row.song_title)
    # )
    # print(f'{query=}')
    entry = query.first()

    if entry is None:
        print(f'no entry found...')
        return

    updated = {
        'title': entry.title,
        'artist': entry.artist
    }

    updated[key] = edit.new_val

    query.update(updated, synchronize_session=False)  # type: ignore

    db.commit()

    # print(f'{edit=}')
    return query.first()


@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    # file_path = os.path.join(app.root_path, "assets")
    file_path = os.path.join(os.path.dirname(__file__), "assets\\favicon.ico")

    # print(f'{file_path=}')
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@app.post("/files_dropped_on_gui", response_model=ReturnType)
# async def files_dropped_on_gui(new_track: Request, db: Session = Depends(get_db)):
async def files_dropped_on_gui(new_tracks: DBSRDroppedFiles, db: Session = Depends(get_db)):
    # new_track.json
    # new_tracks = await new_track.json()
    print(f'files_dropped_on_gui: {new_tracks=} type={type(new_tracks)}')
    paths = new_tracks.file_paths
    if len(paths) == 1 and os.path.isdir(paths[0]):
        paths: list[str] = read_files_from_directory(paths[0])

    # ensure that files are musical in nature, in the future this will convert them to mp3.
    for path in paths:
        if path.endswith('mp3'):
            continue
        elif path.endswith(MUSIC_FILE_EXTENSIONS):
            # TODO: convert the files.
            ...
        else:
            # TODO: if it's an album cover, embed it inside the file.
            ...

    rval = ReturnType()
    # Parse
    for path in paths:
        meta = find_potential_metadata(path)
        # meta['path'] = path
        rval.results.append(meta)
    print(f'{rval=}')
    return rval


# TODO: Formalize a type for req instead of using Request, going to be a list of metadata objects, example in docstring
# @app.post("/submit_song", response_model=ReturnType)
@app.post("/submit_metadata", response_model=Any)
async def submit_metadata(req: Request, db: Session = Depends(get_db)):
    """
    example input:
    metadata = [
        {
            'title': " You're Me and I'm You",
            'artist': 'Black Belt Eagle Scout ',
            'album': None,
            'album_artist': None,
            'acoustid': None,
            'path': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3",
            'key': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3"
        }
    ]
    """
    # first submit it to the db to get the song id.
    metadatas = await req.json()
    # LOG.debug(f'{pp.pformat(metadatas)=}')
    LOG.info(f'{pprint.pp(metadatas)=}')

    # creating a new list of metadata items that are not in db
    # and a list of items that won't be added because they're already in the db
    new_metadatas: Any = []
    old_metadatas: Any = []
    for meta in metadatas:
        # TODO! Improve this query.
        query = db.query(SQLSongMetadata).filter(
            (SQLSongMetadata.artist == meta['artist']) & (
                SQLSongMetadata.title == meta['title'])
        )
        print(f'{query=}')
        if query.first():
            print(f'Cannot add, already an entry in db: {query.first()=}')
            old_metadatas.append(meta)
        else:
            new_metadatas.append(meta)

    # [ ] add the acoustid to the metadata.
    for meta in new_metadatas:
        meta['acoustid'] = generate_acoustid(meta['path'])
    
    for meta in new_metadatas:
        write_metadata_to_file(meta)

    # move them to their new path:
    for meta in new_metadatas:
        try:
            add_file_to_musiclib(meta)
        except Exception as e:
            LOG.debug(f'Failed to move {meta} to a new destination. {e=}')
            # TODO: remove the failed meta from the list. 
    
    
    
    # adding new meta to the db
    for meta in new_metadatas:
        LOG.debug(f'meta new path : {meta["path"]=}')
        new_entry = SQLSongMetadata(
            artist = meta['artist'],
            title = meta['title'],
            file_location = meta['path']
            # acoustid=meta.acoustid,
            # album=meta.album,
            # album_artist=meta.album_artist,
            # path=meta.path
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        meta['id'] = new_entry.id
        print(f'NEW ENTRY: {new_entry.id}')

        # add the new entry to the google drive:
        
    # #     query = db.query(SongMetadata).filter(SongMetadata.id == edit.row.id)

    key_path = 'C:\\Users\\DBS Radio Intern\\code\\pyapi\\app\\credentials\\drive_api_key.json'
    gc = gspread.service_account(filename=key_path) # type: ignore
    sheet = gc.open('test').sheet1  # type: ignore

    # rows: list[list[str]] = []
    for meta in metadatas:
        id, artist, title = meta['id'], meta['artist'], meta['title']
        print(f'sending {title=} {artist=}')
        sheet.append_row([id, artist, title])  # type: ignore

    resp = {
        'added' : new_metadatas,
        'skipped': old_metadatas
    }
    return resp
