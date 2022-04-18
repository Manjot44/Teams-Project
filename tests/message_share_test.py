import requests
from src.config import url

def test_normal_channel_share(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    channel_id2 = create_channel(register_three_users["token"][0], 'CHANNEL_NAME_2', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id2, "dm_id": -1})
    assert response.status_code == 200

def test_normal_dm_share(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": -1, "dm_id": dm_id})
    assert response.status_code == 200

def test_invalid_token(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": "invalid token", "og_message_id": message_id, "message": "Check out this message!", "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 403

def test_invalid_channel_id(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Check out this message!", "channel_id": channel_id + 1, "dm_id": -1})
    assert response.status_code == 400

def test_invalid_dm_id(register_three_users, create_channel, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Check out this message!", "channel_id": -1, "dm_id": dm_id + 1})
    assert response.status_code == 400

def test_length_over_1000(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Sanjam Sang"*1000, "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 400

def test_invalid_message_id(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    channel_id1 = create_channel(register_three_users["token"][0], 'CHANNEL_NAME2', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][1], "og_message_id": message_id + 5, "message": "Wow cool message", "channel_id": channel_id1, "dm_id": -1})
    assert response.status_code == 400

def test_not_in_channel(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][1], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id, "dm_id": -1})
    assert response.status_code == 403

def test_neither_minus_one(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": channel_id, "dm_id": 2})
    assert response.status_code == 400

def test_both_minus_one(register_three_users, create_channel, create_dm, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.post(f"{url}/message/share/v1", json = {"token": register_three_users["token"][0], "og_message_id": message_id, "message": "Wow cool message", "channel_id": -1, "dm_id": -1})
    assert response.status_code == 400