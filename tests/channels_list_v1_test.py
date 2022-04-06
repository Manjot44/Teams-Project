import requests
from src.config import url

def test_invalid_token():
    requests.delete(f"{url}/clear/v1")
    input = {
        "token": "invalidtoken"
    }
    response = requests.get(f"{url}/channels/list/v2", params=input)
    assert response.status_code == 403


def test_single_channel_list(user_init):
    requests.delete(f"{url}/clear/v1")
    auth_response = requests.post(
        f"{url}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    input1 = {
        "token": token,
        "name": "channel1",
        "is_public": True
    }
    requests.post(f"{url}/channels/create/v2", json=input1)
    list_input = {
        "token": token
    }
    response = requests.get(f"{url}/channels/list/v2", params=list_input)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["channels"][0]["channel_id"] == 0
    assert response_data["channels"][0]["name"] == "channel1"


def test_multiple_channel_list(user_init):
    requests.delete(f"{url}/clear/v1")
    auth_response = requests.post(
        f"{url}/auth/register/v2", json=user_init)
    token = auth_response.json()["token"]
    input1 = {
        "token": token,
        "name": "channel1",
        "is_public": True
    }
    requests.post(f"{url}/channels/create/v2", json=input1)
    input2 = {
        "token": token,
        "name": "channel2",
        "is_public": True
    }
    requests.post(f"{url}/channels/create/v2", json=input2)
    list_input = {
        "token": token
    }
    response = requests.get(f"{url}/channels/list/v2", params=list_input)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["channels"][0]["channel_id"] == 0
    assert response_data["channels"][0]["name"] == "channel1"
    assert response_data["channels"][1]["channel_id"] == 1
    assert response_data["channels"][1]["name"] == "channel2"
