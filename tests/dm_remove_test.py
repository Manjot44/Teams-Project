import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"


def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    input = {
        "token": "incorrecttoken",
        "dm_id": 0
    }
    response = requests.delete(f"{BASE_URL}/dm/remove/v1", json=input)
    assert response.status_code == 403


def test_invalid_dm_id(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    auth_response = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    input = {
        "token": token,
        "dm_id": 0
    }
    response = requests.delete(f"{BASE_URL}/dm/remove/v1", json=input)
    assert response.status_code == 400


def test_user_not_in_dm(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user2 = {
        "email": "abcd@gmail.com",
        "password": "thidsIsPass13./",
        "name_first": "Ash",
        "name_last": "Sur"
    }
    user3 = {
        "email": "abcde@gmail.com",
        "password": "thisIsPasss13./",
        "name_first": "Monta",
        "name_last": "Singh"
    }
    auth_response1 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    auth_response2 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user2)
    auth_response3 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user3)
    token1 = auth_response1.json()["token"]
    u_id2 = auth_response2.json()["auth_user_id"]
    token3 = auth_response3.json()["token"]

    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input)

    input1 = {
        "token": token3,
        "dm_id": 0
    }
    response = requests.delete(f"{BASE_URL}/dm/remove/v1", json=input1)
    assert response.status_code == 403


def test_user_not_owner(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user2 = {
        "email": "abcd@gmail.com",
        "password": "thidsIsPass13./",
        "name_first": "Ash",
        "name_last": "Sur"
    }
    auth_response1 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    auth_response2 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user2)
    token1 = auth_response1.json()["token"]
    token2 = auth_response2.json()["token"]
    u_id2 = auth_response2.json()["auth_user_id"]

    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input)

    input1 = {
        "token": token2,
        "dm_id": 0
    }
    response = requests.delete(f"{BASE_URL}/dm/remove/v1", json=input1)
    assert response.status_code == 403


def test_normal(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    user2 = {
        "email": "abcd@gmail.com",
        "password": "thidsIsPass13./",
        "name_first": "Ash",
        "name_last": "Sur"
    }
    auth_response1 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user_init)
    auth_response2 = requests.post(
        f"{BASE_URL}/auth/register/v2", json=user2)
    token1 = auth_response1.json()["token"]
    token2 = auth_response2.json()["token"]
    u_id1 = auth_response1.json()["auth_user_id"]
    u_id2 = auth_response2.json()["auth_user_id"]

    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    dm_create_input2 = {
        "token": token2,
        "u_ids": [u_id1]
    }
    dm_create_data = requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input)
    assert dm_create_data.json()["dm_id"] == 0
    dm_create_data1 = requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input2)
    assert dm_create_data1.json()["dm_id"] == 1
    dm_create_data2 = requests.post(
        f"{BASE_URL}/dm/create/v1", json=dm_create_input)
    assert dm_create_data2.json()["dm_id"] == 2
    rem_input = {
        "token": token1,
        "dm_id": 0
    }
    response = requests.delete(f"{BASE_URL}/dm/remove/v1", json=rem_input)
    assert response.status_code == 200
    dm_list_response = requests.get(
        f"{BASE_URL}/dm/list/v1", params={"token": token1})
    dm_list_data = dm_list_response.json()
    assert dm_list_data["dms"][0]["dm_id"] == 1
    assert dm_list_data["dms"][1]["dm_id"] == 2
