import requests
from src.config import url

def test_invalid_token(reset, register_user):
    auth_response = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    u_id = auth_response.json()["auth_user_id"]
    input = {
        "token": "incorrecttoken",
        "u_ids": [u_id]
    }
    response = requests.post(f"{url}/dm/create/v1", json=input)
    assert response.status_code == 403


def test_duplicate_uid(reset, register_user):
    auth_response = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token = auth_response.json()["token"]
    u_id = auth_response.json()["auth_user_id"]
    input = {
        "token": token,
        "u_ids": [u_id, u_id]
    }
    response = requests.post(f"{url}/dm/create/v1", json=input)
    assert response.status_code == 400


def test_dm_normal(reset, register_user):
    auth_response1 = register_user("jerry@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    auth_response2 = register_user("jerrylin@gmail.com", "thisIsPass13./", "Jerry", "Lin")
    token1 = auth_response1.json()["token"]
    token2 = auth_response2.json()["token"]
    added_user1 = auth_response1.json()["auth_user_id"]
    added_user2 = auth_response2.json()["auth_user_id"]
    input1 = {
        "token": token1,
        "u_ids": [added_user2]
    }
    response1 = requests.post(f"{url}/dm/create/v1", json=input1)
    response_data1 = response1.json()
    assert response1.status_code == 200
    assert response_data1["dm_id"] == 2
    input2 = {
        "token": token2,
        "u_ids": [added_user1]
    }
    response2 = requests.post(f"{url}/dm/create/v1", json=input2)
    response_data2 = response2.json()
    assert response2.status_code == 200
    assert response_data2["dm_id"] == 3
