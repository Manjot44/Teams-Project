import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    input = {
        "token": "invalidtoken"
    }
    response = requests.get(f"{BASE_URL}/dm/list/v1", params=input)
    assert response.status_code == 403


def test_valid_token(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    input = {
        "token": token
    }
    response = requests.get(f"{BASE_URL}/dm/list/v1", params=input)
    assert response.status_code == 200


def test_valid_list(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response1 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token1 = auth_response1.json()["token"]

    user2 = {
        "email": "abcdef@gmail.com",
        "password": "thisIsPss13./",
        "name_first": "Ash",
        "name_last": "Sur"
    }
    auth_response2 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user2)
    u_id2 = auth_response2.json()["auth_user_id"]
    token2 = auth_response2.json()["token"]
    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input)
    input1 = {
        "token": token2
    }
    response = requests.get(f"{BASE_URL}/dm/list/v1", params=input1)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data[0]["dm_id"] == 0
    assert response_data[0]["name"] == "ashsur, jerrylin"
