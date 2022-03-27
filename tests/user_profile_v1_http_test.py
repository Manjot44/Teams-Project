import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_invalid_uid():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": user['token'], "u_id": 10})
    assert response2.status_code == 400


def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": -1, "u_id": user['auth_user_id']})
    assert response2.status_code == 403

def test_correct_return(register_three_users):
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user = response.json()

    response2 = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": user['token'], "u_id": user['auth_user_id']}) 
    assert response2.status_code == 200
    
    assert response2.json() == {'user': {
                                    'u_id': user['auth_user_id'], 
                                    'email': "jerrylin@gmail.com", 
                                    'name_first': 'Jerry', 
                                    'name_last': 'Lin', 
                                    'handle_str': 'jerrylin'
    }}