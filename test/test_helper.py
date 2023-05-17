

from app.helper import (
    write_metadata_to_mp3,
    generate_acoustid,
    convert_m4a_to_mp3
    )

def test_write_metadata_to_mp3():
    meta = {
            'title': "You're Me and I'm You",
            'artist': 'Black Belt Eagle Scout ',
            'album': None,
            'album_artist': None,
            'acoustid': None,
            'path': "D:\\testing\\input\\Black Belt Eagle Scout - At the Party.mp3",
            'key': "D:\\testing\\input\\Black Belt Eagle Scout - At the Party.mp3",
        }
    write_metadata_to_mp3(meta)

def test_generate_acoustid():
    path = "D:\\testing\\input\\Black Belt Eagle Scout - At the Party.mp3"
    acoustid = generate_acoustid(path)
    print(acoustid)

def test_convert_m4a_to_mp3():
    path = "D:\\testing\\input\\01 Riverside (Radio Edit).m4a"
    output = "D:\\testing\\input\\01 Riverside (Radio Edit).mp3"
    new_filename = convert_m4a_to_mp3(path= path, delete_input=False)
    assert output == new_filename
    print(new_filename)