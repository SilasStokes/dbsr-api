import os
from shutil import which
from typing import Any
import mutagen
from mutagen.id3 import (
    ID3,
    TIT2,
    TPE1,
    TALB,
    TXXX, # lets us 
    ID3NoHeaderError
)
import shutil
import acoustid
import subprocess

from app.database import SQLSongMetadata
# local imports:
from .schemas import *
from .global_vars import *

from .log import get_logger
LOG = get_logger(__name__)
LOG.debug("a debug message")


def read_files_from_directory(dirpath: str) -> list[str]:
    file_paths: list[str] = []
    for root, _, files in os.walk(dirpath):
        for f in files:
            file_paths.append(f'{root}\\{f}')
    return file_paths


def _parse_artist_title_album_from_path(path: str) -> Metadata:
    # e.g. D:\music_lib\Music\(Me llamo) Sebastián\El Hambre
    # file: Oye, favorito
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    directory, file = os.path.split(path)
    if file.count('-') == 1:
        artist, title = file.split('-')
    elif file.count('-') == 2:
        artist, album, title = file.split('-')
        album = album.strip()
        # return title, artist
    else:
        artist = directory.split('\\')[-1]
        title = file

    if title.endswith(MUSIC_FILE_EXTENSIONS):
        title = title.split(".")[0]

    return Metadata(artist=artist, title=title, album=album, album_artist=None, acoustid=None, path=path)


def _parse_metadata_from_id3(path: str) -> Metadata:
    # TODO: Check to make sure file exists and supports id3
    # pulling the .mp3 to .wav or whatever else
    file_type = path.split('.')[-1]
    acoustid: str | None = None
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    album_artist: str | None = None
    try:
        mf = mutagen.File(path)  # pyright: ignore
        tags = mf.tags  # pyright: ignore
        match(file_type):
            case 'm4a':
                # notice that getting acoustid for m4a is slightly different than id3 # pyright: ignore
                acoustid = str(tags.get(m4a_acoustid_key, [''])[0])
                title = tags.get(m4a_title_key, [''])[0]  # pyright: ignore
                artist = tags.get(metadata.m4a_artist_key, [''])[
                    0]  # pyright: ignore
                album = tags.get(metadata.m4a_album_key, [''])[
                    0]  # pyright: ignore
                album_artist = tags.get(metadata.m4a_album_artist_key, [''])[
                    0]  # pyright: ignore
            case _:  # id3 which is housed in mp3, wav type files
                # pyright: ignore
                acoustid = str(tags.get(metadata.id3_acoustid_key, ''))
                artist = tags.get(metadata.id3_artist_key, [''])[
                    0]  # pyright: ignore
                title = tags.get(metadata.id3_title_key, [''])[
                    0]  # pyright: ignore
                album = tags.get(metadata.id3_album_key, [''])[
                    0]  # pyright: ignore
                album_artist = tags.get(metadata.id3_album_artist_key, [''])[
                    0]  # pyright: ignore

    except Exception as err:  # pyright: ignore
        pass
        # print(Fore.RED +f"ERROR: {err}, {type(err)=}" + Fore.RESET)
        # usr = input('Press enter: ')

    # type: ignore
    return Metadata(artist=artist, title=title, album=album, album_artist=album_artist, acoustid=acoustid, path=path) # type: ignore


def find_potential_metadata(path: str) -> PotentialMetadatas:
    p_metas = PotentialMetadatas(
        filename=path, type=path.split('.')[-1], potentialMetadata=[])
    p_metas.potentialMetadata.append(_parse_artist_title_album_from_path(path))
    p_metas.potentialMetadata.append(_parse_metadata_from_id3(path))
    return p_metas


def move(src: str, dst: str):
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(dst)

        # copy file
    shutil.copy2(src=src, dst=dst)

def add_file_to_musiclib(meta: Any) -> None:
    """
    :param meta: a dictionary that contains a path, artist and title field to generate a path with
    :returns: None
    """
    dst_folder = os.path.join(MUSIC_LIB_PATH, meta['artist'])

    dst_filename = f'{meta["artist"]} - {meta["title"]}'

    LOG.debug(
        f'moving {meta["path"]} to {os.path.join(dst_folder, dst_filename)}')
    meta['path'] = os.path.join(dst_folder, dst_filename)
    # shutil.copy2(meta['path'], os.path.join(dst_folder, dst_filename))


def generate_acoustid(path: str) -> str:
    try:
        _, acoustid_bytes = acoustid.fingerprint_file(path)  # type: ignore
        acoustid_string = acoustid_bytes.decode('utf-8')  # type: ignore
    except Exception as err:
        LOG.error(f'ERROR generating acoustid: {err}, {type(err)=} on {path}')
        acoustid_string = ''
    return acoustid_string  # type: ignore

def write_metadata_to_mp3(meta: Any) -> None:
    """
    meta object should look like:
        {
            'title': " You're Me and I'm You",
            'artist': 'Black Belt Eagle Scout ',
            'album': None,
            'album_artist': None,
            'acoustid': None,
            'path': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3",
            'key': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3"
        }
    """
    if not meta['path'].endswith('.mp3'):
        return
    
    try: 
        tags = ID3(meta.get('path', '')) # type: ignore
    except ID3NoHeaderError: # type: ignore
        print('id3 error')
        tags = ID3() # type: ignore
    
    if not meta.get('acoustid', None):
        meta['acoustid'] = generate_acoustid(meta['path'])

    tags.add(TXXX(encoding=3, desc='Acoustid Fingerprint',text=meta['acoustid'])) # type: ignore

    if meta.get('title', None):
        tags.add(TIT2(encoding=3, text=meta.get('title', '')))  # type: ignore
    if meta.get('artist', None):
        tags.add(TPE1(encoding=3, text=meta.get('artist', '')))  # type: ignore
    if meta.get('album', None):
        tags.add(TALB(encoding=3, text=meta.get('album', '')))  # type: ignore

    tags.save(meta['path']) # type: ignore

def convert_m4a_to_mp3(path: str, delete_input: bool = True) -> str:
    """
    used `choco install ffmpeg-full` 
    """
    if not which('ffmpeg'):
        raise Exception('ffmpeg not installed')

    output = os.path.splitext(path)[0] + '.mp3'

    try:
        subprocess.call(['ffmpeg', '-y', '-i', path, output]) 

        if delete_input:
            os.remove(path)
    except Exception as e:
        LOG.error(f'error: {e}')
        raise e
    
    return output

def send_SQLSongMetadata_to_googledrive(meta: SQLSongMetadata) -> None:
    ...
