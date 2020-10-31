

def test_list(video, client, user_headers):
    res = client.get('/tutorials', headers=user_headers)

    assert res.status_code == 200
    assert len(res.get_json()) == 1

def test_new_video(user, client, user_headers):
    res = client.post('/tutorials', json={
        'name': 'Видео 2',
        'description': 'Опиулмку'
    }, headers= user_headers)
    assert res.status_code == 200
    assert res.get_json()['name'] == "Видео 2"


def test_edit_video(video, client, user_headers):
    res = client.put(
        f'/tutorials/1',
        json={
            'name': "Видео 321",
            'description': 'klweflk'
        },
        headers=user_headers)
    assert res.status_code == 200