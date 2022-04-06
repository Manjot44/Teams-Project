import requests
import pytest
import src.config

def test_correct_output():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()
    
    response2 =  requests.put(f"{src.config.url}/user/profile/setemail/v1", json = {"token": user1["token"], "email": "montajree@gmail.com"})  
    assert response2.status_code == 200

    response3 = requests.get(f"{src.config.url}/user/profile/v1", params = {"token": user1["token"], "u_id": user1["auth_user_id"]}) 

    return_val = response3.json()
    assert return_val == {'user': {
                                    'u_id': user1['auth_user_id'], 
                                    'email': "montajree@gmail.com", 
                                    'name_first': 'Jerry', 
                                    'name_last': 'Lin', 
                                    'handle_str': 'jerrylin'
    }}

def test_invalid_new_email():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{src.config.url}/user/profile/setemail/v1", json = {"token": user1["token"], "email": "montajree.com"})
    assert response2.status_code == 400   

def test_email_already_in_use():    
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "manjotbhathal@gmail.com", "password": "ManjotBhathal4", "name_first": "Manjot", "name_last": "Bhathal"})
    assert response2.status_code == 200 

    response3 = requests.put(f"{src.config.url}/user/profile/setemail/v1", json = {"token": user1["token"], "email": "manjotbhathal@gmail.com"})
    assert response3.status_code == 400  

def test_invalid_token():
    requests.delete(f"{src.config.url}/clear/v1")

    response = requests.post(f"{src.config.url}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200 

    response2 = requests.put(f"{src.config.url}/user/profile/setemail/v1", json = {"token": "invalid token", "email": "montajree@gmail.com"})
    assert response2.status_code == 403       