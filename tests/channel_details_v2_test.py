import pytest
import requests
from src import auth, channel, channels, error, data_store, other

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8181
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_channel_details_valid_user_public_channel(register_three_users):
    requests.delete(f"{BASE_URL}/clear/v1")
    
    token = register_three_users['id'][0]
    response = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': token,
        'name': 'channel_name',
        'is_public': True
    })
    channel = response.json()
    channel_id = channel['channel_id']
    response = requests.get(f"{BASE_URL}/channel/details/v2&token={token}&channel_id={channel_id}")
    assert response.status_code == 200
    
    details = response.json()
    assert details['name'] == 'channel_name'
    assert details['is_public'] == True
    owner = register['id'][0]
    assert details['owner_members'] == [
        {
            'u_id': owner,
            'email': 'aBc123._%+-@aBc123.-.Co',
            'name_first': 'A',
            'name_last': 'A',
            'handle_str': 'AA',
        }
    ]
    assert details['all_members'] == [
        {
            'u_id': owner,
            'email': 'aBc123._%+-@aBc123.-.Co',
            'name_first': 'A',
            'name_last': 'A',
            'handle_str': 'AA',
        }
    ]

def test_channel_details_invalid_token_valid_channel(register_three_users):
    requests.delete(f"{BASE_URL}/clear/v1")
    token = register_three_users['token'][0]
    response = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': token,
        'name': 'channel_name',
        'is_public': True,
    })
    channel = response.json()
    valid_channel_id = channel['channel_id']
    invalid_token = None
    response = requests.get(f"{BASE_URL}/channel/details/v2?token={invalid_token}&channel_id={valid_channel_id}")
    assert response.status_code == 403

def test_channel_details_invalid_token_invalid_channel():
    requests.delete(f"{BASE_URL}/clear/v1")
    invalid_token = None
    invalid_channel_id = None
    response = requests.get(f"{BASE_URL}/channel/details/v2?token={invalid_token}&channel_id={invalid_channel_id}")
    assert response.status_code == 403

def test_channel_details_valid_token_invalid_channel(register_three_users):
    requests.delete(f"{BASE_URL}/clear/v1")
    valid_token = register_three_users['token'][0]
    invalid_channel_id = None
    response = requests.get(f"{BASE_URL}/channel/details/v2?token={valid_token}&channel_id={invalid_channel_id}")
    assert response.status_code == 400

def test_channel_details_valid_channel_user_not_member(register_three_users):
    requests.delete(f"{BASE_URL}/clear/v1")
    member_token = register_three_users['token'][0]
    nonmember_token = register_three_users['token'][1]
    response = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': member_token,
        'name': 'channel_name',
        'is_public': True,
    })
    channel = response.json()
    channel_id = channel['channel_id']
    parameters = '?token={nonmember_token}&channel_id={channel_id}'
    response = requests.get(f"{BASE_URL}/channel/details/v2{parameters}")
    assert response.status_code == 403