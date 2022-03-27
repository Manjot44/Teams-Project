import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 7777
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_dm_leave_input_error_valid_token_invalid_dm_id(register_three_users):
    token = register_three_users['token'][0]
    dm_id = None
    response = requests.post(f"{BASE_URL}/dm/leave/v1", json={'token': token, 'dm_id': dm_id})
    assert response.status_code == 400

def test_dm_leave_invalid_token_valid_dm_id(register_three_users):
    invalid_token = None
    valid_token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    #run dm create with one user to another user
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': valid_token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    #run dm leave with wrong token and dm_id
    response = requests.post(f"{BASE_URL}/dm/leave/v1", json={'token': invalid_token, 'dm_id': dm_id['dm_id']})
    assert response.status_code == 403

def test_dm_leave_access_error_valid_dm_id_user_not_member(register_three_users):
    nonmember_token = register_three_users['token'][2]
    member_token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    #run dm create with one user to another user
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': member_token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    dm_id = dm_id['dm_id']
    #run dm leave with wrong token and dm_id
    response = requests.post(f"{BASE_URL}/dm/leave/v1", json={'token': nonmember_token, 'dm_id': dm_id})
    assert response.status_code == 403

def test_dm_leave_valid_input_creator_leaving(register_three_users):
    leaver_token = register_three_users['token'][0]
    member_id = register_three_users['id'][1]
    response = requests.post(f"{BASE_URL}/dm/create/v1", json={'token': leaver_token, 'u_ids': [member_id]})
    assert response.status_code == 200
    dm_id = response.json()
    dm_id = dm_id['dm_id']
    response = requests.post(f"{BASE_URL}/dm/leave/v1", json={'token': leaver_token, 'dm_id': dm_id})
    assert response.status_code == 200
    member_token = register_three_users['token'][1]
    response = requests.get(f"{BASE_URL}/dm/details/v1?token={member_token}&dm_id={dm_id}")
    assert response.status_code == 200
    details = response.json()
    assert len(details['members']) == 1