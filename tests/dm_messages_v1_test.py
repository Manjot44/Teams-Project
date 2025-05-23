import requests
from src.config import url

''' dm/messages/v1  {token, dm_id, start} 
                    {messages, start, end} '''

def test_dm_messages_dm_id_invalid(register_three_users):
    token = register_three_users['token'][0]
    dm_id = None
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id}&start={start}")
    assert response.status_code == 400

def test_initialised_dmid_invalid(register_three_users):
    requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users['token'][0], "u_ids": [register_three_users['id'][1]]})
    dm_id = None
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={register_three_users['token'][0]}&dm_id={dm_id}&start={start}")
    assert response.status_code == 400

def test_dm_messages_start_invalid_0_messages(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 1
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 400

def test_dm_messages_start_invalid_2_messages(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    response = requests.post(f"{url}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': "Your"
    })
    assert response.status_code == 200
    member_token = register_three_users['token'][1]
    response = requests.post(f"{url}/message/senddm/v1", json={
        'token': member_token,
        'dm_id': dm_id['dm_id'],
        'message': "Mother"
    })
    assert response.status_code == 200
    start = 3
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 400

def test_dm_messages_dm_id_valid_user_not_member(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 0
    nonmember_token = register_three_users['token'][2]
    response = requests.get(f"{url}/dm/messages/v1?token={nonmember_token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 403

def test_dm_messages_token_invalid_dm_id_valid(register_three_users):
    token = None
    valid_token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': valid_token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 403

def test_dm_messages_token_invalid_dm_id_invalid(register_three_users):
    token = None
    dm_id = None
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id}&start={start}")
    assert response.status_code == 403

def test_dm_messages_valid_input(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    response = requests.post(f"{url}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': "Your"
    })
    assert response.status_code == 200
    member_token = register_three_users['token'][1]
    response = requests.post(f"{url}/message/senddm/v1", json={
        'token': member_token,
        'dm_id': dm_id['dm_id'],
        'message': "Mother"
    })
    assert response.status_code == 200
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 200
    
def test_over_50_messages(register_three_users, create_dm, send_messagedm):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{url}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    
    i = 0
    while i < 60:
        response = requests.post(f"{url}/message/senddm/v1", json={
            'token': token,
            'dm_id': dm_id['dm_id'],
            'message': "Your"
        })
        assert response.status_code == 200
        i += 1

    assert response.status_code == 200
    start = 0
    response = requests.get(f"{url}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 200