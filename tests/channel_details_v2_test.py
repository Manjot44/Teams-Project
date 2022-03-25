import pytest
import requests
from src import auth, channel, channels, error, data_store, other

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8181
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_details_valid_user_public_channel(register_three_users):
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
    assert details['owner_members'] == ['{owner}']
    assert details['all_members'] == ['{owner}']

