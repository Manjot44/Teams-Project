import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_message_senddm_dm_id_invalid_token_valid(register_three_users):    # 400
    token = register_three_users['token'][0]
    dm_id = None
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={'token': token, 'dm_id': dm_id, 'message': 'Message will not send'})
    assert response.status_code == 400

def test_message_senddm_message_len_1001(register_three_users):             # 400
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    message = "W" * 1001
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': message
    })
    assert response.status_code == 400

def test_message_senddm_message_len_0(register_three_users):                # 400
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    message = ""
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': message
    })
    assert response.status_code == 400

def test_message_senddm_dm_id_valid_user_not_member(register_three_users):  # 403
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    invalid_token = register_three_users['token'][2]
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': invalid_token,
        'dm_id': dm_id['dm_id'],
        'message': 'Knock, knock'
    })
    assert response.status_code == 403

def test_message_senddm_token_invalid_dm_id_valid(register_three_users):    # 403
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    invalid_token = None
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': invalid_token,
        'dm_id': dm_id['dm_id'],
        'message': 'Knock, knock'
    })
    assert response.status_code == 403
    
def test_message_senddm_token_invalid_dm_id_invalid(register_three_users):  # 403
    token = None
    dm_id = None
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id,
        'message': 'Knock, knock'
    })
    assert response.status_code == 403

def test_message_senddm_message_len_1000(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    message = "W" * 1000
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': message
    })
    assert response.status_code == 200


def test_message_senddm_message_len_1(register_three_users):
    token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    message = "W"
    response = requests.post(f"{BASE_URL}/message/senddm/v1", json={
        'token': token,
        'dm_id': dm_id['dm_id'],
        'message': message
    })
    assert response.status_code == 200

