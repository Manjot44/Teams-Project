import requests
from src.config import url

def test_invalid_token(reset):
    input = {
        "token": "invalidtoken",
        "dm_id": 0
    }
    response = requests.get(f"{url}/dm/details/v1", params=input)
    assert response.status_code == 403


def test_invalid_dm_id(reset, register_user):
    requests.delete(f"{url}/clear/v1")
    auth_response = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token = auth_response.json()["token"]
    input = {
        "token": token,
        "dm_id": 0
    }
    response = requests.get(f"{url}/dm/details/v1", params=input)
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
    response = requests.get(f"{url}/dm/details/v1", params=input1)
    assert response.status_code == 403


def test_normal(reset, register_user):
    auth_response1 = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token1 = auth_response1.json()["token"]

    auth_response2 = register_user("jerrylin@gmail.com", "thisIsPass13./", "Ash", "Sur")
    u_id2 = auth_response2.json()["auth_user_id"]
    token2 = auth_response2.json()["token"]
    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    new_dm = requests.post(f"{url}/dm/create/v1", json=dm_create_input)
    dm_id = new_dm.json()["dm_id"]
    input1 = {
        "token": token2,
        "dm_id": dm_id
    }
    response = requests.get(f"{url}/dm/details/v1", params=input1)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == 'ashsur, jerrylin'
    assert len(response_data["members"]) == 2
