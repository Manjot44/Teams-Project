import requests
from src.config import url


def test_long_name(user_init):
    requests.delete(f"{url}/clear/v1")
    auth_response2 = requests.post(
        f"{url}/auth/register/v2", json=user_init)
    token1 = auth_response2.json()["token"]
    input = {
        "token": token1,
        "name": "12345678klmopqrstuvwx",
        "is_public": False
    }
    response = requests.post(f"{url}/channels/create/v2", json=input)
    assert response.status_code == 400


def test_short_name(user_init):
    requests.delete(f"{url}/clear/v1")
    auth_response2 = requests.post(
        f"{url}/auth/register/v2", json=user_init)
    token1 = auth_response2.json()["token"]
    input = {
        "token": token1,
        "name": "12345678klmopqrstuvwx",
        "is_public": False
    }
    response = requests.post(f"{url}/channels/create/v2", json=input)
    assert response.status_code == 400


def test_normal_dualchannel(user_init):
    requests.delete(f"{url}/clear/v1")
    user = {
        "email": "aBc123._%+-@aBc123.-.Co",
        "password": "123456",
        "name_first": "A",
        "name_last": "A"
    }
    auth_response1 = requests.post(f"{url}/auth/register/v2", json=user)
    token1 = auth_response1.json()["token"]
    input1 = {
        "token": token1,
        "name": "channel1",
        "is_public": False
    }
    response1 = requests.post(f"{url}/channels/create/v2", json=input1)
    assert response1.status_code == 200
    response_data1 = response1.json()
    assert response_data1["channel_id"] == 0
    auth_response2 = requests.post(
        f"{url}/auth/register/v2", json=user_init)
    token2 = auth_response2.json()["token"]
    input2 = {
        "token": token2,
        "name": "channel2",
        "is_public": True
    }
    response2 = requests.post(f"{url}/channels/create/v2", json=input2)
    assert response2.status_code == 200
    response_data2 = response2.json()
    assert response_data2["channel_id"] == 1


def test_invalid_token():
    requests.delete(f"{url}/clear/v1")
    input = {
        "token": "invalidtoken",
        "name": "channel1",
        "is_public": True
    }
    response = requests.post(f"{url}/channels/create/v2", json=input)
    assert response.status_code == 403
