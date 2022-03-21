import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# as other functions have not yet been written, I will be writing a draft of the tests 
# i will test these as other functions become complete

def test_valid_leave(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = {"token:": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channel/leave/v1", json = {"token:": register_three_users["token"][0], "channel_id": channel_id})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channel/details/v2", json = {"token:": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 200
    response_data = response.json()
    owner_members = response_data["owner_members"]
    all_members = response_data["all_members"]
    
    for member in owner_members:
        assert member["u_id"] != register_three_users["id"][0]
    for member in all_members:
        assert member["u_id"] != register_three_users["id"][0]

def test_invalid_channel_id(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200

    response = requests.post(f"{BASE_URL}/channel/leave/v1", json = {"token:": register_three_users["token"][0], "channel_id": None})
    assert response.status_code == 400

def test_non_member_leave(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/channel/leave/v1", json = {"token:": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 403

def test_invalid_token_registered(register_three_users):
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = {"token:": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{BASE_URL}/channel/leave/v1", json = {"token:": None, "channel_id": channel_id})
    assert response.status_code == 403

def test_invalid_token_unregistered():
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/channel/leave/v1", json = {"token:": None, "channel_id": 0})
    assert response.status_code == 403
