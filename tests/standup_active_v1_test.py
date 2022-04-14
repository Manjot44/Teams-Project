from ssl import CHANNEL_BINDING_TYPES
import requests
from src.config import url

def test_standup_active_channel_standup_inactive(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.get(f"{url}standup/active/v1?token={token}&channel_id={channel}")
    assert response.status_code == 200
    data = response.json()
    assert data['is_active'] == False
    assert data['time_finish'] == None

def test_standup_active_channel_standup_active_20sec(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 20})
    assert response.status_code == 200
    data = response.json()
    time_finish = data['time_finish']
    response = requests.get(f"{url}standup/active/v1?token={token}&channel_id={channel}")
    assert response.status_code == 200
    data = response.json()
    assert data['is_active'] == True
    assert data['time_finish'] == time_finish

def test_standup_active_channelid_invalid(register_three_users):
    token = register_three_users['token'][0]
    response = requests.get(f"{url}standup/active/v1?token={token}&channel_id={None}")
    assert response.status_code == 400

def test_standup_active_channelid_valid_user_not_member(register_three_users, create_channel):
    member = register_three_users['token'][0]
    nonmember = register_three_users['token'][1]
    channel = create_channel(member, 'CHANNEL_NAME', True)
    response = requests.get(f"{url}standup/active/v1?token={nonmember}&channel_id={channel}")
    assert response.status_code == 403

def test_standup_active_token_invalid(register_three_users):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.get(f"{url}standup/active/v1?token={None}&channel_id={channel}")
    assert response.status_code == 403

def test_standup_active_token_invalid_channelid_invalid(register_three_users):
    response = requests.get(f"{url}standup/active/v1?token={None}&channel_id={None}")
    assert response.status_code == 403
