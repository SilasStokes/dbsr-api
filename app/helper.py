import os

import mutagen

# local imports:
from .models import *
from .schemas import *
from .global_vars import *

def read_files_from_directory(dirpath: str) -> list[str]:
    file_paths: list[str] = []
    
    for root, _, files in os.walk(dirpath):
        for f in files:
            file_paths.append(f'{root}\\{f}')
    
    return file_paths

def _parse_artist_title_album_from_path(path: str) -> Metadata :
    # e.g. D:\music_lib\Music\(Me llamo) Sebastián\El Hambre
    # file: Oye, favorito
    title : str | None = None
    artist : str | None = None
    album : str | None = None
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
    
    return Metadata( artist = artist, title= title, album = album, album_artist=None, acoustid = None, path=path)

def _parse_metadata_from_id3(path: str) -> Metadata:
    #TODO: Check to make sure file exists and supports id3
    file_type = path.split('.')[-1] # pulling the .mp3 to .wav or whatever else
    acoustid : str | None =  None
    title : str | None =  None
    artist : str | None =  None
    album : str | None =  None
    album_artist : str | None =  None
    try:
        mf = mutagen.File(path) # pyright: ignore
        tags = mf.tags # pyright: ignore
        match(file_type):
            case 'm4a':
                acoustid = str(tags.get(m4a_acoustid_key, [''])[0]) # notice that getting acoustid for m4a is slightly different than id3 # pyright: ignore
                title =  tags.get(m4a_title_key, [''])[0] # pyright: ignore
                artist = tags.get(metadata.m4a_artist_key, [''])[0] # pyright: ignore
                album = tags.get(metadata.m4a_album_key, [''])[0] # pyright: ignore
                album_artist =  tags.get(metadata.m4a_album_artist_key, [''])[0] # pyright: ignore
            case _: # id3 which is housed in mp3, wav type files
                acoustid = str(tags.get(metadata.id3_acoustid_key, '')) # pyright: ignore
                artist = tags.get(metadata.id3_artist_key, [''])[0]  # pyright: ignore
                title =  tags.get(metadata.id3_title_key, [''])[0] # pyright: ignore
                album = tags.get(metadata.id3_album_key, [''])[0] # pyright: ignore
                album_artist =  tags.get(metadata.id3_album_artist_key, [''])[0] # pyright: ignore       
                
    except Exception as err: # pyright: ignore
        pass
        # print(Fore.RED +f"ERROR: {err}, {type(err)=}" + Fore.RESET)
        # usr = input('Press enter: ') 
    
    return Metadata( artist = artist, title= title, album = album, album_artist=album_artist, acoustid = acoustid, path=path) # type: ignore

def find_potential_metadata(path: str) -> PotentialMetadatas:
    
    p_metas = PotentialMetadatas(filename=path, type=path.split('.')[-1] , potentialMetadata=[])

    p_metas.potentialMetadata.append(_parse_artist_title_album_from_path(path))
    
    p_metas.potentialMetadata.append(_parse_metadata_from_id3(path))
    
    return p_metas