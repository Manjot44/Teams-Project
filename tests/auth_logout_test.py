import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# as other functions have not yet been written, I will be writing a draft of the tests 
# i will test these as other functions become complete

def test_valid_logout(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    response_data['auth_user_id'] == register_three_users["id"][0]
    second_token = response_data["token"]
    
    response = requests.post(f"{BASE_URL}/auth/logout/v1", json = {"token": register_three_users["token"][0]})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": second_token, "name": "channel_name", "is_public": True})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 403

def test_invalid_token_regitistered():
    
