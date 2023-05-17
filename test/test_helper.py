

import pytest

from app.helper import write_metadata_to_mp3

# @pytest.fixture
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