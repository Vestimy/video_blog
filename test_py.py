from app import client
from models import Video


def test_get():
    res = client.get('/tutorials')

    assert res.status_code == 200
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'name': 'Video #3 PyTest',
        'description': 'Checked'
    }
    res = client.post('/tutorials', json=data)

    assert res.status_code == 200
    # assert len(res.get_json()) == 3
    assert res.get_json()['name'] == 'Video #3 PyTest'


def test_put():
    res = client.put('/tutorials/1', json={'name': 'UDP'})

    assert res.status_code == 200

    assert Video.query.get(1).name == 'UDP'




def test_delete():

    res = client.delete('/tutorials/6')

    assert res.status_code == 204

    assert Video.query.get(6) is None