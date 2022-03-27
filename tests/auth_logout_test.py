import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


def test_valid_logout(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users["id"][0]
    second_token = response_data["token"]
    
    response = requests.post(f"{BASE_URL}/auth/logout/v1", json = {"token": register_three_users["token"][0]})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": second_token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 403

def test_invalid_token_registered(register_three_users):
    response = requests.post(f"{BASE_URL}/auth/logout/v1", json = {"token": None})
    assert response.status_code == 403

def test_invalid_token_unregistered():
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/auth/logout/v1", json = {"token": None})
    assert response.status_code == 403
