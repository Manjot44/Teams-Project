import requests
import src.config

def test_invalid_token(register_three_users):
    response = requests.get(f"{src.config.url}search/v1?token=invalidtoken&query_str=hello")
    assert response.status_code == 403

def test_inavlid_small_query(register_three_users):
    response = requests.get(f"{src.config.url}search/v1?token={register_three_users['token'][1]}&query_str=")
    assert response.status_code == 400

def test_invalid_large_query(register_three_users):
    large_query = "h" * 1001
    response = requests.get(f"{src.config.url}search/v1?token={register_three_users['token'][1]}&query_str={large_query}")
    assert response.status_code == 400

def test_valid_filter_2_messages(register_three_users, create_channel):
    channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    
    message_info = {
        'token': register_three_users["token"][0],
        'channel_id': channel_id,
        'message': "hello there"
    }
    response = requests.post(f"{src.config.url}/message/send/v1", json = message_info)
    assert response.status_code == 200
    message_id = response.json()['message_id']

    message_info['message'] = "hell"
    requests.post(f"{src.config.url}/message/send/v1", json = message_info)

    response = requests.get(f"{src.config.url}search/v1?token={register_three_users['token'][0]}&query_str=hello")
    assert response.status_code == 200
    
    returned_message_id = response.json()['messages'][0]['message_id']
    assert message_id == returned_message_id

def test_only_joined_channels_searched(register_three_users, create_channel, invite_to_channel):
    searched_messages = []
    
    created_channel_id = create_channel(register_three_users["token"][0], "channel_name", True)
    message_info = {
        'token': register_three_users["token"][0],
        'channel_id': created_channel_id,
        'message': "hello JErrY1./23"
    }
    response = requests.post(f"{src.config.url}/message/send/v1", json = message_info)
    assert response.status_code == 200
    message_id = response.json()['message_id']
    searched_messages.append(message_id)

    other_channel_id = create_channel(register_three_users["token"][1], "channel_name", True)
    message_info['token'] = register_three_users['token'][1]
    message_info['channel_id'] =  other_channel_id
    requests.post(f"{src.config.url}/message/send/v1", json = message_info)

    invited_channel_id = create_channel(register_three_users["token"][2], "channel_name", True)
    invite_to_channel(register_three_users["token"][2], invited_channel_id, register_three_users["id"][0])
    message_info['token'] = register_three_users['token'][2]
    message_info['channel_id'] = invited_channel_id

    response = requests.post(f"{src.config.url}/message/send/v1", json = message_info)
    assert response.status_code == 200
    message_id = response.json()['message_id']
    searched_messages.append(message_id)

    response = requests.get(f"{src.config.url}search/v1?token={register_three_users['token'][0]}&query_str=jerry1.")
    assert response.status_code == 200
    messages = response.json()['messages']

    for message in messages:
        assert message['message_id'] in searched_messages

def test_dm_message_search(register_three_users, create_dm, send_messagedm):
    dm_id = create_dm(register_three_users["token"][2], [])
    message_id = send_messagedm(register_three_users["token"][2], dm_id, "hello my name is jerry")
    requests.post(f"{src.config.url}/message/react/v1", json = {"token": register_three_users["token"][2], "message_id": message_id, "react_id": 1})

    response = requests.get(f"{src.config.url}search/v1?token={register_three_users['token'][2]}&query_str=NAME")
    assert response.status_code == 200
    message = response.json()['messages'][0]

    assert message['message_id'] == message_id
