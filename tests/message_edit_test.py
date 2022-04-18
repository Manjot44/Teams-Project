import requests
from src.config import url

# Test if message edit works as it should 
def test_valid_edit(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "Hello Rahman Noodles"})
    assert response.status_code == 200

# Test if "message" is empty
def test_empty_message(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": ""})
    assert response.status_code == 200

# Test if message_id is invalid
def test_invalid_message_id(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id + 20, "message": "Hello Iqti"})
    assert response.status_code == 400

# TO DO: write a test that inputs a >1000 character long message
def test_message_too_long(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "iqtidar"*1000})
    assert response.status_code == 400

# Test - Message not sent by the authorised user making a request: AccesError
def test_not_from_user(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][1], "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 403

# Test - User did not send the message, but is an owner member, should go through
def test_not_from_user_owner(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    
    response = requests.post(f"{url}/channel/join/v2", json = {"token": register_three_users["token"][1], "channel_id": channel_id})
    assert response.status_code == 200

    message_id = send_message(register_three_users["token"][1], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 200

# User making request does not have a valid token:
def test_invalid_user_id(register_three_users, create_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], 'CHANNEL_NAME', True)
    message_id = send_message(register_three_users["token"][0], channel_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": 'invalid token', "message_id": message_id, "message": "Hello Iqti"})
    assert response.status_code == 403

# Test if message edit can edit a dm message as it should
def test_edit_dm(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0], register_three_users["id"][1]])
    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "Hello Rahman Noodles"})
    assert response.status_code == 200

# Test if an empty dm is input as one of the arguments - should delete dm
def test_empty_dm(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0]])
    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": ""})
    assert response.status_code == 200

# Test - User did not send the message, but is an owner member, should go through (for DMs)
def test_dm_not_from_user(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0], register_three_users["id"][1]])
    message_id = send_messagedm(register_three_users["token"][1], dm_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][0], "message_id": message_id, "message": "doctor sureshkumar I got a heart attack"})
    assert response.status_code == 200

# test - unauthorised person cant edit dm
def test_dm_unauthorised(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][0], register_three_users["id"][1]])

    message_id = send_messagedm(register_three_users["token"][0], dm_id, "Hello Sanjam")

    response = requests.put(f"{url}/message/edit/v1", json = {"token": register_three_users["token"][1], "message_id": message_id, "message": "doctor sureshkumar I got a heart attack"})
    assert response.status_code == 403
