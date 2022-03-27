import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# as other functions have not yet been written, I will be writing a draft of the tests 
# i will test these as other functions become complete

def test_valid_message(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200

def test_invalid_channel(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": "landejend", "message": "Hello Sanjam"})
    assert response.status_code == 400

def test_bad_message(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": None})
    assert response.status_code == 400

def test_not_user(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 403

def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": None, "channel_id": 0, "message": "Hello Sanjam"})
    assert response.status_code == 403
