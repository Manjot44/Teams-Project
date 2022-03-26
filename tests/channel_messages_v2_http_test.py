import requests
import pytest

BASE_ADDRESS = 'http://127.0.0.1'
BASE_PORT = 8080
BASE_URL = f"{BASE_ADDRESS}:{BASE_PORT}"

def test_invalid_channel_id():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()['token']

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': token1, 'channel_id': "invalid channel_id", 'start': 0})
    assert response3.status_code == 400

def test_user_invalid():  
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]
    response2 = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "manjotbhathal@gmail.com", "password": "ManJoTBhathAl4", "name_first": "Manjot", "name_last": "Bhathal"})    
    token2 = response2.json()["token"]
   
    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response3 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response3.json()['channel_id']

    response4 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': token2, 'channel_id': channel_id, 'start': 0})
    assert response4.status_code == 403

def test_valid_start_no_messages():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': token1, 'channel_id': channel_id, 'start': 10})
    assert response3.status_code == 400

def test_valid_start():
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': token1, 'channel_id': channel_id, 'start': 0})
    assert response3.status_code == 200

def test_user_registered():  
    requests.delete(f"{BASE_URL}/clear/v1")

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': "unregistered user", 'channel_id': channel_id, 'start': 0})
    assert response3.status_code == 403

def test_invalid_token():
    requests.delete(f"{BASE_URL}/clear/v1")   

    response = requests.post(f"{BASE_URL}/auth/register/v2", json={"email": "jerrylin@gmail.com", "password": "JerrYlin4", "name_first": "Jerry", "name_last": "Lin"})
    token1 = response.json()["token"]

    input = {
        "token": token1,
        "name": "foo",
        "is_public": True
    }

    response2 = requests.post(f"{BASE_URL}/channels/create/v2", json=input)
    channel_id = response2.json()['channel_id']

    response3 = requests.get(f"{BASE_URL}/channel/messages/v2", json={'token': "invalid token", 'channel_id': channel_id, 'start': 0})
    assert response3.status_code == 403 