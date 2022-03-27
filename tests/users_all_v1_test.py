import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_users_all_token_invalid(register_three_users):
    token = None
    response = requests.get(f"{BASE_URL}/users/all/v1?token={token}")
    assert response.status_code == 403

def test_users_all_token_valid(register_three_users):
    token = register_three_users['token'][0]
    response = requests.get(f"{BASE_URL}/users/all/v1?token={token}")
    assert response.status_code == 200
    users_all = response.json()
    assert users_all['users'][0]['u_id'] == register_three_users['id'][0]
    assert users_all['users'][1]['u_id'] == register_three_users['id'][1]
    assert users_all['users'][2]['u_id'] == register_three_users['id'][2]


# def test_users_all_all_fields(register_three_users):
#     token = register_three_users['token'][0]
#     u_id = register_three_users['id'][0]
#     response = requests.get(f"{BASE_URL}/user/profile/v1?token={token}&u_id={u_id}")
#     assert response.status_code == 200
#     profile = response.json()
#     response = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": token, "u_id": u_id}) 
#     assert response.status_code == 200
#     users_all = response.json()
#     assert profile == 457
#     assert users_all['users'][0] == profile['user']

def test_users_all_all_fields():
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()
    response2 = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": user['token'], "u_id": user['auth_user_id']}) 
    assert response2.status_code == 200
    profile = response2.json()
    response = requests.get(f"{BASE_URL}/users/all/v1?token={user['token']}")
    assert response.status_code == 200
    users_all = response.json()
    assert users_all['users'][0] == {'email': 'jerrylin@gmail.com', 'handle_str': 'jerrylin', 'name_first': 'Jerry', 'name_last': 'Lin', 'u_id': 0}