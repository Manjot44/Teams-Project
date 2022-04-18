import requests
import src.config

# ADD MESSAGE REACT TESTS IN ONCE THAT IS COMPLETE

def test_invalid_token(register_three_users):
    response = requests.get(f"{src.config.url}/notifications/get/v1?token=invalidtoken")
    assert response.status_code == 403

def test_get_channeladd_notification(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][1])
    
    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][1]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']

    expected_response = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': "aa added you to channel_name"
    }

    assert notifications[0] == expected_response

def test_get_dmadd_notification(register_three_users, create_dm):
    dm_id = create_dm(register_three_users["token"][0], [register_three_users["id"][2]])

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']

    expected_response = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': "aa added you to aa, jerrylin"
    }

    assert notifications[0] == expected_response

def test_get_channeltag_notification(register_three_users, create_channel, invite_to_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][2])

    message_info = {
        'token': register_three_users["token"][0],
        'channel_id': channel_id,
        'message': "@jerrylin hello there"
    }
    response = requests.post(f"{src.config.url}/message/send/v1", json = message_info)

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']

    expected_response = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': "aa tagged you in channel_name: @jerrylin hello ther"
    }

    assert notifications[0] == expected_response

def test_get_dmtag_notification(register_three_users, create_dm):
    dm_id = create_dm(register_three_users["token"][2], [])

    message_info = {
        'token': register_three_users["token"][2],
        'dm_id': dm_id,
        'message': "@jerrylin"
    }
    response = requests.post(f"{src.config.url}/message/senddm/v1", json = message_info)

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']

    expected_response = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': "jerrylin tagged you in jerrylin: @jerrylin"
    }

    assert notifications[0] == expected_response

def test_valid_handle_not_in_specific_channeldm(register_three_users, create_channel, create_dm, send_message, send_messagedm):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    dm_id = create_dm(register_three_users["token"][0], [])

    send_message(register_three_users["token"][0], channel_id, "@jerrylin")
    send_messagedm(register_three_users["token"][0], dm_id, "@jerrylin")

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']
    expected_response = []
    assert notifications == expected_response

def test_valid_react(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][2], [])
    message_id = send_messagedm(register_three_users["token"][2], dm_id, "hello my name is jerry")

    requests.post(f"{src.config.url}/message/react/v1", json = {"token": register_three_users["token"][2], "message_id": message_id, "react_id": 1})

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications'][0]
    expected_response = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': "jerrylin reacted to your message in jerrylin"
    }
    assert notifications == expected_response


def test_react_after_channel_leave(register_three_users, create_channel, invite_to_channel, send_message):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    invite_to_channel(register_three_users["token"][0], channel_id, register_three_users["id"][2])

    message_id1 = send_message(register_three_users["token"][2], channel_id, "hello my name is lin")
    message_id2 = send_message(register_three_users["token"][2], channel_id, "jerry lin")
    
    requests.post(f"{src.config.url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id1, "react_id": 1})
    requests.post(f"{src.config.url}/channel/leave/v1", json = {"token": register_three_users["token"][2], "channel_id": channel_id})
    requests.post(f"{src.config.url}/message/react/v1", json = {"token": register_three_users["token"][0], "message_id": message_id2, "react_id": 1})

    response = requests.get(f"{src.config.url}/notifications/get/v1?token={register_three_users['token'][2]}")
    assert response.status_code == 200
    notifications = response.json()['notifications']
    assert len(notifications) == 2