import pytest
import requests
from src import auth, channel, channels, error, data_store, other

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_listall_invalid_user():
    requests.delete(f"{BASE_URL}/clear/v1")
    token = None
    response = requests.get(f"{BASE_URL}/channels/listall/v2?token={token}")
    assert response.status_code == 403
    
def test_listall_valid_user_no_channel():
    # CLEAR
    requests.delete(f"{BASE_URL}/clear/v1")
    # REGISTER USER # later use the three users fixture
    response = requests.post(f"{BASE_URL}/auth/register/v2", json={'email': 'email@email.com', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    response_data = response.json()
    token = response_data['token']
    # START LISTALL TESTING
        # Test if request is received
    response = requests.get(f"{BASE_URL}/channels/listall/v2?token={token}")
    assert response.status_code == 200
        # Test data returned
    response_data = response.json()
    assert response_data['channels'] == []
    assert len(response_data['channels']) == 0

def test_listall_valid_user_1_public_channel():
    requests.delete(f"{BASE_URL}/clear/v1")
    # REGISTER USER # later use the three user fixture    
    response = requests.post(f"{BASE_URL}/auth/register/v2", json={'email': 'email@email.com', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    auth_register = response.json()
    token = auth_register['token']
    # CREATE PUBLIC CHANNEL
    response = requests.post(f"{BASE_URL}/channels/create/v2", json={
        'token': token,
        'name': 'channel_name',
        'is_public': True
    })
    channel_id = response.json()
    # TEST LISTALL FOR CHANNEL
    response = requests.get(f"{BASE_URL}/channels/listall/v2?token={token}")
    assert response.status_code == 200
    # TEST DATA RETURNED
    channel = response.json()
    assert channel['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel['channels'][0]['name'] == 'channel_name'
    #assert channel['channels'][0]['owner_members'][0]['u_id'] == u_id
    

def test_listall_valid_user_3_public_channel():
    pass

def test_listall_valid_user_1_private_channel():
    pass

def test_listall_valid_user_1_public_1_private_channel():
    pass
