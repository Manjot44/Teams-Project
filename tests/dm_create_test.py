import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


def test_invalid_token(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    u_id = auth_response.json()["auth_user_id"]
    input = {
        "token": "incorrecttoken",
        "u_ids": [u_id]
    }
    response = requests.post(f"{BASE_URL}/dm/create/v1", json=input)
    assert response.status_code == 403


def test_invalid_uid(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    input = {
        "token": token,
        "u_ids": []
    }
    response = requests.post(f"{BASE_URL}/dm/create/v1", json=input)
    assert response.status_code == 400


def test_duplicate_uid(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    u_id = auth_response.json()["auth_user_id"]
    input = {
        "token": token,
        "u_ids": [u_id, u_id]
    }
    response = requests.post(f"{BASE_URL}/dm/create/v1", json=input)
    assert response.status_code == 400


def test_dm_normal(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response1 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token = auth_response1.json()["token"]
    new_user = {
        "email": "abcdewf@gmail.com",
        "password": "thisI=ljhs13./",
        "name_first": "zsh",
        "name_last": "Sur"
    }
    auth_response2 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=new_user)
    added_user = auth_response2.json()["auth_user_id"]
    input = {
        "token": token,
        "u_ids": [added_user]
    }
    response = requests.post(f"{BASE_URL}/dm/create/v1", json=input)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["dm_id"] == 0
