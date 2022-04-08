import requests
from src.config import url


def test_invalid_token(reset):
    input = {
        "token": "incorrecttoken",
        "dm_id": 0
    }
    response = requests.delete(f"{url}/dm/remove/v1", json=input)
    assert response.status_code == 403


def test_invalid_dm_id(reset, register_user):
    auth_response = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token = auth_response.json()["token"]
    input = {
        "token": token,
        "dm_id": 0
    }
    response = requests.delete(f"{url}/dm/remove/v1", json=input)
    assert response.status_code == 400


def test_user_not_in_dm(register_three_users):
    token1 = register_three_users["token"][0]
    u_id2 = register_three_users["id"][1]
    token3 = register_three_users["token"][2]

    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    response = requests.post(f"{url}/dm/create/v1", json=dm_create_input)
    dm_id = response.json()["dm_id"]

    input1 = {
        "token": token3,
        "dm_id": dm_id
    }
    response = requests.delete(f"{url}/dm/remove/v1", json=input1)
    assert response.status_code == 403


def test_user_not_owner(reset, register_user):
    auth_response1 = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    auth_response2 = register_user("jerrylin@gmail.com", "thisIsPass13./", "Ash", "Sur")
    token1 = auth_response1.json()["token"]
    token2 = auth_response2.json()["token"]
    u_id2 = auth_response2.json()["auth_user_id"]

    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    response = requests.post(f"{url}/dm/create/v1", json=dm_create_input)
    dm_id = response.json()["dm_id"]

    input1 = {
        "token": token2,
        "dm_id": dm_id
    }
    response = requests.delete(f"{url}/dm/remove/v1", json=input1)
    assert response.status_code == 403


def test_normal(reset, register_user):
    auth_response1 = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    auth_response2 = register_user("jerrylin@gmail.com", "thisIsPass13./", "Ash", "Sur")
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
    dm_create_data = requests.post(f"{url}/dm/create/v1", json=dm_create_input)
    assert dm_create_data.json()["dm_id"] == 2
    
    dm_create_data1 = requests.post(f"{url}/dm/create/v1", json=dm_create_input2)
    assert dm_create_data1.json()["dm_id"] == 3
    
    dm_create_data2 = requests.post(f"{url}/dm/create/v1", json=dm_create_input)
    assert dm_create_data2.json()["dm_id"] == 4
    
    rem_input = {
        "token": token1,
        "dm_id": 2
    }
    response = requests.delete(f"{url}/dm/remove/v1", json=rem_input)
    assert response.status_code == 200
    dm_list_response = requests.get(f"{url}/dm/list/v1", params={"token": token1})
    dm_list_data = dm_list_response.json()
    assert dm_list_data["dms"][0]["dm_id"] == 3
    assert dm_list_data["dms"][1]["dm_id"] == 4
