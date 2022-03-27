import pytest
import requests
from src.messages import message_send_v1
from tests.conftest import register_three_users

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# Test if message edit works as it should 
def test_valid_edit(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "Hello Rahman Noodles"})
    assert response.status_code == 200

# Test if "message" is empty
def test_empty_message(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": None})
    assert response.status_code == 200

# Test if message_id is invalid
def test_invalid_message_id(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id + 20, "message": "Hello Iqti"})
    assert response.status_code == 400

# TO DO: write a test that inputs a >1000 character long message
def test_message_too_long(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "iqtidar"*1000})
    assert response.status_code == 400

# Test - Message not sent by the authorised user making a request: AccesError
def test_not_from_user(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][1], "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 403

# Test - User did not send the message, but is an owner member, should go through
def test_not_from_user_owner(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]
    
    response = requests.post(f"{BASE_URL}/channel/join/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 200

# User making request does not have a valid token:
def test_invalid_user_id(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.put(f"{BASE_URL}/message/edit/v1", json = {"token": 'invalid token', "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 403