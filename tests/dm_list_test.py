import requests
from src.config import url


def test_invalid_token(reset):
    input = {
        "token": "invalidtoken"
    }
    response = requests.get(f"{url}/dm/list/v1", params=input)
    assert response.status_code == 403


def test_valid_token(reset, register_user):
    auth_response = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token = auth_response.json()["token"]
    input = {
        "token": token
    }
    response = requests.get(f"{url}/dm/list/v1", params=input)
    assert response.status_code == 200


def test_valid_list(reset, register_user):
    auth_response1 = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token1 = auth_response1.json()["token"]

    auth_response2 = register_user("jerrylin@gmail.com", "thisIsPass13./", "Ash", "Sur")
    u_id2 = auth_response2.json()["auth_user_id"]
    token2 = auth_response2.json()["token"]
    dm_create_input = {
        "token": token1,
        "u_ids": [u_id2]
    }
    requests.post(
        f"{url}/dm/create/v1", json=dm_create_input)
    input1 = {
        "token": token2
    }
    response = requests.get(f"{url}/dm/list/v1", params=input1)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["dms"][0]["dm_id"] == 2
    assert response_data["dms"][0]["name"] == "ashsur, jerrylin"
