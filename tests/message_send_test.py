import pytest
import requests
import src.config

def test_valid_message(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200

def test_invalid_channel(register_three_users, create_channel):
    create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": "landejend", "message": "Hello Sanjam"})
    assert response.status_code == 400

def test_bad_message(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": None})
    assert response.status_code == 400

def test_not_user(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 403

def test_invalid_token(reset):
    response = requests.post(f"{src.config.url}/message/send/v1", json = {"token": None, "channel_id": 0, "message": "Hello Sanjam"})
    assert response.status_code == 403
