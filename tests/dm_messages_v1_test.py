import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 7777
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

''' dm/messages/v1  {token, dm_id, start} 
                    {messages, start, end} '''

def test_dm_messages_dm_id_invalid(register_three_users):
    token = register_three_users['token'][0]
    dm_id = None
    start = 0
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={token}&dm_id={dm_id}&start={start}")
    assert response.status_code == 400

def test_dm_messages_start_invalid_0_messages(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 1
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 400

def test_dm_messages_start_invalid_2_messages(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    response = requests.post(f"{BASE_URL}/dm/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': "Your"
    })
    assert response.status_code == 200
    member_token = register_three_users['token'][1]
    response = requests.post(f"{BASE_URL}/dm/senddm/v1", json={
        'token': member_token,
        'dm_id': dm_id['dm_id'],
        'message': "Mother"
    })
    assert response.status_code == 200
    start = 2
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 400

def test_dm_messages_dm_id_valid_user_not_member(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 0
    nonmember_token = register_three_users['token'][2]
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={nonmember_token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 403

def test_dm_messages_token_invalid_dm_id_valid(register_three_users):
    token = None
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    start = 0
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={token}&dm_id={dm_id['dm_id']}&start={start}")
    assert response.status_code == 403

def test_dm_messages_token_invalid_dm_id_invalid(register_three_users):
    token = None
    dm_id = None
    start = 0
    response = requests.get(f"{BASE_URL}/dm/messages/v1?token={token}&dm_id={dm_id}&start={start}")
    assert response.status_code == 403