import pytest
import requests
import src.config

def test_valid_message(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200

def test_invalid_channel(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": "landejend", "message": "Hello Sanjam"})
    assert response.status_code == 400

def test_bad_message(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": None})
    assert response.status_code == 400

def test_not_user(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 403

def test_invalid_token():
    requests.delete(f"{src.config.url}/clear/v1")
    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": None, "channel_id": 0, "message": "Hello Sanjam"})
    assert response.status_code == 403
