from fastapi.testclient import TestClient


from .main import app
from .log import get_logger

LOG = get_logger(__name__)

client = TestClient(app)


def test_submit_metadata():
    resp = client.post("/submit_metadata", json=[
        {
            'title': "You're Me and I'm You",
            'artist': 'Black Belt Eagle Scout ',
            'album': None,
            'album_artist': None,
            'acoustid': None,
            'path': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3",
                    'key': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3"
        }
    ])
    LOG.error(f'test_submit_metadata call {resp=}')
    assert resp.status_code == 200
    # assert resp.json() == "success"
