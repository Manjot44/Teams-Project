import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

# as other functions have not yet been written, I will be writing a draft of the tests 
# i will test these as other functions become complete

def test_valid_logout(register_three_users):
    
    response = requests.post(f"{BASE_URL}/auth/logout/v1", json = {"token": register_three_users["token"][0]})
