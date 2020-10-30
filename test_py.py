from app import client


def test_get():
    res = client.get('/tutorials')

    assert res.status_code == 200
    assert len(res.get_json()) == 2
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'id': 3,
        'name': 'Video #3 PyTest',
        'description': 'Checked'
    }
    res = client.post('/tutorials', json=data)

    assert res.status_code == 200
    assert len(res.get_json()) == 3
    assert res.get_json()[-1]['name'] == 'Video #3 PyTest'


def test_put():
    data = {
        'name': 'Video #3 PyTest Edit',
        'description': 'Checked V2'
    }
    res = client.put('/tutorials/3', json=data)
    assert res.status_code == 200

    assert res.get_json()['name'] == data['name']




def test_delete():
    pass