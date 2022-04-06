import pytest
import requests
import src.config

def test_valid_add(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][1], "channel_name", True)

    invite_to_channel(register_three_users["token"][1], channel_id, register_three_users["id"][0])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][0]})
    assert response.status_code == 200

    response = requests.get(f"{src.config.url}/channel/details/v2?token={register_three_users['token'][0]}&channel_id={channel_id}")
    assert response.status_code == 200
    response_data = response.json()
    owner_members = response_data["owner_members"]

    is_owner = False
    for owner in owner_members:
        if owner["u_id"] == register_three_users["id"][0]:
            is_owner = True
    assert is_owner

def test_invalid_channel(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": None, "u_id": register_three_users["id"][1]})
    assert response.status_code == 400

def test_invalid_uid(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": None})
    assert response.status_code == 400

def test_invalid_member(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 400

def test_already_owner(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 200

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 400

def test_invalid_permissions(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])
    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][2])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "u_id": register_three_users["id"][2]})
    assert response.status_code == 403

def test_invalid_token_registered(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)

    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])

    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": None, "channel_id": channel_id, "u_id": register_three_users["id"][1]})
    assert response.status_code == 403

def test_invalid_token_unregistered(reset):
    response = requests.post(f"{src.config.url}/channel/addowner/v1", json = {"token": None, "channel_id": 0, "u_id": 0})
    assert response.status_code == 403
