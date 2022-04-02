import pytest
import requests
import src.config

def test_valid_remove(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 200
    
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 200

    response = requests.get(f"{src.config.url}/channel/details/v2?token={register_three_users['token'][0]}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    owner_members = response_data["owner_members"]

    for owner in owner_members:
        assert owner["u_id"] != register_three_users["id"][2]

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][2], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200
    
def test_invalid_channel(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200
    
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][1], "channel_id": None, "u_id": register_three_users["id"][0]})
    assert response.status_code == 400

def test_invalid_uid(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200
    
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": None})
    assert response.status_code == 400

def test_not_owner(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 400

def test_only_owner(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    assert response.status_code == 400

def test_invalid_permissions(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200
    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 200
    
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": register_three_users["token"][2], "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    assert response.status_code == 403

def test_invalid_token_registered(register_three_users):
    response = requests.post(f"{src.config.url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{src.config.url}/channel/invite/v2", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200
    
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": None, "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    assert response.status_code == 403

def test_invalid_token_unregistered():
    requests.delete(f"{src.config.url}/clear/v1")
    response = requests.post(f"{src.config.url}/channel/removeowner/v1", json = {"token": None, "channel_id": 0, "u_id": 0})
    assert response.status_code == 403
