import pytest
import requests
import src.config

def test_authlog_valid(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users["id"][0]

    user_init['email'] = ".@..Ml"
    user_init['password'] = "a>?:1#"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['auth_user_id'] == register_three_users["id"][1]

def test_incorrect_details(register_three_users, user_init):
    user_init['email'] = "aBc12._%+-@aBc123.-.Co"
    user_init['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "1234576"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400                 

def test_empty(register_three_users, user_init):
    user_init['email'] = ""
    user_init['password'] = "123456"
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400

    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = ""   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400                        

def test_mixed_password(register_three_users, user_init):
    user_init['email'] = "aBc123._%+-@aBc123.-.Co"
    user_init['password'] = "a>?:1#"   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400                        
    
    user_init['email'] = ".@..Ml"
    user_init['password'] = "123456"   
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400                                                            

def test_no_registered_user(user_init):
    requests.delete(f"{src.config.url}/clear/v1")
    response = requests.post(f"{src.config.url}/auth/login/v2", json = user_init)
    assert response.status_code == 400
