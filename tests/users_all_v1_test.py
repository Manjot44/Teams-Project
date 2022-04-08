import requests
from src.config import url

def test_users_all_token_invalid(register_three_users):
    token = None
    response = requests.get(f"{url}/users/all/v1?token={token}")
    assert response.status_code == 403

def test_users_all_token_valid(register_three_users):
    token = register_three_users['token'][0]
    response = requests.get(f"{url}/users/all/v1?token={token}")
    assert response.status_code == 200
    users_all = response.json()
    assert users_all['users'][0]['u_id'] == register_three_users['id'][0]
    assert users_all['users'][1]['u_id'] == register_three_users['id'][1]
    assert users_all['users'][2]['u_id'] == register_three_users['id'][2]

def test_users_all_all_fields():
    requests.delete(f"{url}/clear/v1")
    response = requests.post(f"{url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()
    response = requests.get(f"{url}/users/all/v1?token={user['token']}")
    assert response.status_code == 200
    users_all = response.json()
    assert users_all['users'][0] == {'email': 'jerrylin@gmail.com', 'handle_str': 'jerrylin', 'name_first': 'Jerry', 'name_last': 'Lin', 'u_id': 0}