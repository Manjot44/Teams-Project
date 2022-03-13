import pytest
import requests

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_authlog_valid(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users[0]

    user_init['email'] = ".@..Ml"
    user_init['password'] = "a>?:1#"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users[1]

def test_incorrect_details(register_three_users, user_init):
    user_init['email'] = "aBc12._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "1234576"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400                 

def test_empty(register_three_users, user_init):
    user_init['email'] = ""
    user_init['password'] = "123456"
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = ""   
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400                        

def test_mixed_password(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "a>?:1#"   
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400                        
    
    user_init['email'] = ".@..Ml"
    user_init['password'] = "123456"   
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400                                                            

def test_no_registered_user(user_init):
    requests.delete(f"{BASE_URL}/clear/v1")
    response = requests.post(f"{BASE_URL}/auth/login/v2", json = user_init)
    assert response.status_code == 400 