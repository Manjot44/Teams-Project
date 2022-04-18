from time import sleep
import requests
from src.config import url

def test_standup_send_input_valid_1message_og_user(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = 'message from og'
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    time_finish = response.json()
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': channel, 'message': message})
    assert response.status_code == 200
    sleep(5)
    response = requests.get(f"{url}channel/messages/v2?token={token}&channel_id={channel}&start=0")
    assert response.status_code == 200
    data = response.json()
    assert data['messages'][0]['time_sent'] == time_finish['time_finish']

def test_standup_send_input_valid_2message_2user(register_three_users, create_channel):
    token0 = register_three_users['token'][0]
    token1 = register_three_users['token'][2]
    id1 = register_three_users['id'][2]
    channel = create_channel(token0, 'CHANNEL_NAME', True)
    message1 = 'message from og'
    message2 = 'message from 2nd'
    response = requests.post(f"{url}channel/invite/v2", json={'token': token0, 'channel_id': channel, 'u_id': id1})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/start/v1", json={'token': token0, 'channel_id': channel, 'length': 5})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': token0, 'channel_id': channel, 'message': message1})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': token1, 'channel_id': channel, 'message': message2})
    assert response.status_code == 200

def test_standup_send_message_len_1000(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = 'P' * 1000
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': channel, 'message': message})
    assert response.status_code == 200

def test_standup_send_message_len_0(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = ''
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': channel, 'message': message})
    assert response.status_code == 200

def test_standup_send_channelid_invalid(register_three_users):
    token = register_three_users['token'][0]
    message = 'message from og'
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': None, 'message': message})
    assert response.status_code == 400

def test_standup_send_message_len_over1000(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = 'P' * 1001
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': channel, 'message': message})
    assert response.status_code == 400

def test_standup_send_standup_inactive(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = 'message from og'
    response = requests.post(f"{url}standup/send/v1", json={'token': token, 'channel_id': channel, 'message': message})
    assert response.status_code == 400

def test_standup_send_channelid_valid_user_not_member(register_three_users, create_channel):
    member = register_three_users['token'][0]
    nonmember = register_three_users['token'][1]
    channel = create_channel(member, 'CHANNEL_NAME', True)
    message = 'message from og'
    response = requests.post(f"{url}standup/start/v1", json={'token': member, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': nonmember, 'channel_id': channel, 'message': message})
    assert response.status_code == 403

def test_standup_send_token_invalid_channelid_valid(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    message = 'message from og'
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 2})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/send/v1", json={'token': None, 'channel_id': channel, 'message': message})
    assert response.status_code == 403

def test_standup_send_token_invalid_channelid_invalid(register_three_users):
    message = 'message from og'
    response = requests.post(f"{url}standup/send/v1", json={'token': None, 'channel_id': None, 'message': message})
    assert response.status_code == 403
