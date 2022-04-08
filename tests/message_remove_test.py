import requests
from src.config import url

# Test if message remove works as it should 
def test_valid_remove(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200

# Test for invalid token
def test_invalid_token(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": "incorrect token", "message_id": message_id})
    assert response.status_code == 403

# Test for invalid message_id
def test_invalid_message_id(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][0], "message_id": message_id + 20})
    assert response.status_code == 400

# Test - Message not sent by the authorised user making a request: AccesError
def test_not_form_user(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][0], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][1], "message_id": message_id})
    assert response.status_code == 403

# Test - User did not send the message, but is an owner member, should go through
def test_not_from_user_owner(register_three_users):
    response = requests.post(f"{url}/channels/create/v2", json = {"token": register_three_users["token"][0], "name": "channel_name", "is_public": True})
    assert response.status_code == 200
    response_data = response.json()
    channel_id = response_data["channel_id"]

    response = requests.post(f"{url}/channel/join/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 200

    response = requests.post(f"{url}/message/send/v1", json = {"token": register_three_users["token"][1], "channel_id": channel_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200

# test if it removes a dm as it should
def test_remove_dm_normal(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0], register_three_users["id"][1]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    response = requests.post(f"{url}/message/senddm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][0], "message_id": message_id})
    assert response.status_code == 200

# test where unauthorised person tried to remove dm
def test_remove_unauthrosied(register_three_users):
    response = requests.post(f"{url}/dm/create/v1", json = {"token": register_three_users["token"][0], "u_ids": [register_three_users["id"][0], register_three_users["id"][1]]})
    assert response.status_code == 200
    response_data = response.json()
    dm_id = response_data["dm_id"]

    response = requests.post(f"{url}/message/senddm/v1", json = {"token": register_three_users["token"][0], "dm_id": dm_id, "message": "Hello Sanjam"})
    assert response.status_code == 200
    response_data = response.json()
    message_id = response_data["message_id"]

    response = requests.delete(f"{url}/message/remove/v1", json = {"token": register_three_users["token"][1], "message_id": message_id})
    assert response.status_code == 403