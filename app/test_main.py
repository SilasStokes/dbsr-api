from fastapi.testclient import TestClient


from main import app

client = TestClient(app)


def test_submit_metadata():
    resp = client.post("/submit_metadata", json=[
        {
            'title': " You're Me and I'm You",
            'artist': 'Black Belt Eagle Scout ',
            'album': None,
            'album_artist': None,
            'acoustid': None,
            'path': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3",
                    'key': "C:\\Users\\DBS Radio Intern\\code\\electron-exploration\\dbsr_gui\\test_songs\\input\\Black Belt Eagle Scout - You're Me and I'm You.mp3"
        }
    ])
    print(f'{resp=}')
    assert resp == "success"
