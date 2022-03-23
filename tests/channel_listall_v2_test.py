import pytest
import requests
from src import auth, channel, channels, error, data_store, other

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_listall_invalid_user():
    invalid_id = None
    
def test_listall_valid_user_no_channel():
    # Register user
    response = requests.post(f"{BASE_URL}/auth/register/v2", json={'email': 'email@email.com', 'password': 'password', 'name_first': 'first', 'name_last': 'last'})
    response_data = response.get_json()
    token = response_data['token']
    # Start listall testing 
        # Test if request is received
    response = requests.get(f"{BASE_URL}/channels/listall/v2&token={token}")
    assert response.status_code == 200
        # Test data returned
    response_data = response.get_json()
    assert response_data['channels'] == []
    assert len(response_data['channels']) == 0
