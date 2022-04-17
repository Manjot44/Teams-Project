import requests
from src.config import url

# REGULAR SEASON TESTS
def test_standup_start_standup_period_0_sec(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 0})
    assert response.status_code == 200
    

def test_standup_start_standup_period_5_sec(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 5})
    assert response.status_code == 200
    response = response.json()
    response['time_finish']

def test_standup_start_standup_period_5_sec_mtpl_users(register_three_users, create_channel, invite_to_channel):
    token0 = register_three_users['token'][0]
    token1 = register_three_users['token'][1]
    u_id1 = register_three_users['id'][1]
    channel = create_channel(token0, 'CHANNEL_NAME', True)
    invite_to_channel(token1, channel, u_id1)
    response = requests.post(f"{url}standup/start/v1", json={'token': token0, 'channel_id': channel, 'length': 0})
    assert response.status_code == 200
    



# PRE SEASON TESTS - INPUT ERR
def test_standup_start_channelid_invalid(register_three_users):
    token = register_three_users['token'][0]
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': None, 'length': 5})
    assert response.status_code == 400

def test_standup_start_standup_period_neg_1_sec(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': -1})
    assert response.status_code == 400

def test_standup_start_active_standup_running(register_three_users, create_channel):
    token = register_three_users['token'][0]
    channel = create_channel(token, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 10})
    assert response.status_code == 200
    response = requests.post(f"{url}standup/start/v1", json={'token': token, 'channel_id': channel, 'length': 10})
    assert response.status_code == 400

# PRE SEASON TESTS - ACCESS ERR
def test_standup_start_channel_id_valid_user_not_member(register_three_users, create_channel):
    member = register_three_users['token'][0]
    nonmember = register_three_users['token'][1]
    channel = create_channel(member, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': nonmember, 'channel_id': channel, 'length': 10})
    assert response.status_code == 403

def test_standup_start_token_invalid_rest_valid(register_three_users, create_channel):
    member = register_three_users['token'][0]
    channel = create_channel(member, 'CHANNEL_NAME', True)
    response = requests.post(f"{url}standup/start/v1", json={'token': None, 'channel_id': channel, 'length': 10})
    assert response.status_code == 403 

def test_standup_start_token_invalid_rest_invalid(register_three_users):
    response = requests.post(f"{url}standup/start/v1", json={'token': None, 'channel_id': None, 'length': None}) 
    assert response.status_code == 403
    
# figure out how to do timestamps but jsut test the status code for now