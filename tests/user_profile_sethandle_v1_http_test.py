import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_correct_output():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()
    
    response2 =  requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": user1["token"], "handle_str": "manjotbhathal"})  
    assert response2.status_code == 200

    response3 = requests.get(f"{BASE_URL}/user/profile/v1", params = {"token": user1["token"], "u_id": user1["auth_user_id"]}) 

    return_val = response3.json()
    assert return_val == {'user': {
                                    'u_id': user1['auth_user_id'], 
                                    'email': "jerrylin@gmail.com", 
                                    'name_first': 'Jerry', 
                                    'name_last': 'Lin', 
                                    'handle_str': 'manjotbhathal'
    }}

def test_invalid_handle_length1():  
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": user1["token"], "handle_str": "manjotbhathalmanjotbhathalmanjotbhathalmanjotbhathal"})
    assert response2.status_code == 400

def test_invalid_handle_length2():  
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": user1["token"], "handle_str": "m"})
    assert response2.status_code == 400   

def test_invalid_handle_character_type():    
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": user1["token"], "handle_str": "manjot!@#&*()-+"})
    assert response2.status_code == 400  

def test_handle_already_in_use():    
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    user1 = response.json()

    response2 = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "manjotbhathal@gmail.com", "password": "ManjotBhathal4", "name_first": "Manjot", "name_last": "Bhathal"})
    assert response2.status_code == 200 

    response3 = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": user1["token"], "handle_str": "manjotbhathal"})
    assert response3.status_code == 400 

def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json = {"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    assert response.status_code == 200

    response2 = requests.put(f"{BASE_URL}/user/profile/sethandle/v1", json = {"token": "invalid token", "handle_str": "manjotbhathal"})
    assert response2.status_code == 403