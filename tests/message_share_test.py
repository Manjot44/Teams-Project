import requests
from src.config import url

def test_normal_channel_share(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name2", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id2 = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id2, "dm_id": -1})
    assert response.status_code == 200

def test_normal_dm_share(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": -1, "dm_id": dm_id})
    assert response.status_code == 200

def test_invalid_token(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": "invalid token", "og_message_id": message_id, "message": "Check out this message!", "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 403

def test_invalid_channel_id(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Check out this message!", "channel_id": channel_id + 1, "dm_id": -1})
    assert response.status_code == 400

def test_invalid_dm_id(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    response = requests.post(f"{url}/message/senddm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Check out this message!", "channel_id": -1, "dm_id": dm_id + 1})
    assert response.status_code == 400

def test_length_over_1000(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Sanjam Sang"*1000, "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 400

def test_invalid_message_id(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][1], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id1 = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][1], "og_message_id": message_id + 5, "message": "Wow cool message", "channel_id": channel_id1, "dm_id": -1})
    assert response.status_code == 400

def test_not_in_channel(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][1], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 403

def test_neither_minus_one(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id, "dm_id": 2})
    assert response.status_code == 400

def test_both_minus_one(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": -1, "dm_id": -1})
    assert response.status_code == 400